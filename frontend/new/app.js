document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const questionInput = document.getElementById("question-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", function() {
        const question = questionInput.value;
        if (question.trim() === "") {
            alert("Please enter a question.");
            return;
        }
        askQuestion(question);
    });

    function askQuestion(question) {
        const sessionId = localStorage.getItem("session_id") || generateSessionId();
        localStorage.setItem("session_id", sessionId);

        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        })
        .then(response => response.text())
        .then(data => {
            const p = document.createElement("p");
            p.textContent = data;
            chatBox.appendChild(p);
            questionInput.value = "";
        })
        .catch(error => console.error("Error:", error));
    }

    function generateSessionId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
});
