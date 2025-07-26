document.getElementById("analyzeBtn").addEventListener('click', analyzeText);

function analyzeText() {
    const text = document.getElementById("inputText").value;

    if (!text.trim()) {
        document.getElementById("result").innerText = "Please enter some text.";
        return
    }

    fetch("https://sentiment-analysis-dyxp.onrender.com/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerText = data.error
                return;
            }

            let resultHTML = `
    <h3>Sentiment: ${data.sentiment}</h3>
    <p>Score: ${data.score.toFixed(2)}</p>
`;

            document.getElementById("result").innerHTML = resultHTML;
        }).catch(err => {
            document.getElementById("result").innerText = "Error contacting backend";
            console.error(err);
        });
}