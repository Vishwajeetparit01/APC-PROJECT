
const chat = document.getElementById("chat");
const input = document.getElementById("message");
const form = document.getElementById("chat-form");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    input.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(data.reply || "Something went wrong.", "bot");
        } else {
            addMessage(data.reply, "bot");
        }
    } catch (error) {
        addMessage("Could not connect to the chatbot. Please check the Flask server.", "bot");
    } finally {
        input.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage();
});

function askQuestion(question) {
    input.value = question;
    sendMessage();
}

function clearChat() {
    chat.innerHTML = "";
    addMessage("Chat cleared! How can I help you?", "bot");
}

async function showHistory() {
    try {
        const response = await fetch("/history");
        const history = await response.json();

        if (!history.length) {
            addMessage("No chat history available yet.", "bot");
            return;
        }

        history.forEach(item => {
            addMessage("You: " + item.question, "user");
            addMessage(item.answer, "bot");
        });
    } catch (error) {
        addMessage("Unable to load chat history.", "bot");
    }
}
