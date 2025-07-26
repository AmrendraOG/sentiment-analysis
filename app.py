import string
from flask import Flask, request, jsonify, render_template
from collections import Counter
import nltk
import os

nltk_data_path = os.path.join(os.getcwd(), "nltk_data")

nltk.data.path.append(nltk_data_path)

def safe_nltk_download():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', download_dir=nltk_data_path)

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', download_dir=nltk_data_path)

    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', download_dir=nltk_data_path)

safe_nltk_download()


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)

def analyze_text(text, emotion_file='emotions.txt'):
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")
    filtered = [word for word in tokenized_words if word not in stopwords.words('english')]

    emotion_list = []
    with open(emotion_file, 'r') as file:
        for line in file:
            clear_line = line.translate(str.maketrans('', '', "'\n,")).strip()
            if ':' in clear_line:
                word, emotion = clear_line.split(':')
                if word in filtered:
                    emotion_list.append(emotion.strip())

    return filtered, emotion_list, cleaned_text


def get_sentiment(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    if score['neg'] > score['pos']:
        return "Negative 😔", score['neg']
    elif score['pos'] > score['neg']:
        return "Positive 😀", score['pos']
    else:
        return "Neutral 😐", score['neu']


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"error": "Text is empty"}), 400
    
    filtered_words, emotions, cleaned_text = analyze_text(text)
    sentiment, score = get_sentiment(cleaned_text)
    emotion_count = dict(Counter(emotions))

    return jsonify({
        "sentiment": sentiment,
        "score": score,
        "emotions": emotion_count
    })


if __name__ == '__main__':
    app.run(debug=True)