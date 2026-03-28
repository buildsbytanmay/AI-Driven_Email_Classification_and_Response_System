function checkLogin() {
    const loggedIn = document.cookie.includes("logged_in=true");

    if (!loggedIn) {
        window.location.href = "/login";
    }
}

let currentEmailId = null;

// Load Inbox
async function loadInbox() {
    const res = await fetch("/emails/unread");
    const data = await res.json();

    const list = document.getElementById("emailList");
    list.innerHTML = "<h3>Inbox</h3>";

    data.forEach(email => {
        const div = document.createElement("div");
        div.className = "email-item";

        div.innerHTML = `
            <strong>${email.sender}</strong><br>
            ${email.subject}<br>
            <small>${email.snippet}</small>
        `;

        div.onclick = () => openEmail(email.id);

        list.appendChild(div);
    });
}

// Open Email
async function openEmail(id) {
    currentEmailId = id;

    const res = await fetch(`/emails/${id}`);
    const data = await res.json();

    document.getElementById("sender").innerText = data.sender || "";
    document.getElementById("subject").innerText = data.subject || "";
    document.getElementById("body").innerText = data.body;
}

// Generate AI Reply
async function generateReply() {
    const res = await fetch(`/emails/${currentEmailId}/generate-reply`, {
        method: "POST"
    });

    const data = await res.json();

    document.getElementById("replyBox").value = data.reply;
}

// Custom Reply
async function customReply() {
    const instruction = document.getElementById("customInput").value;

    const res = await fetch(`/emails/${currentEmailId}/custom-reply`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ instruction })
    });

    const data = await res.json();

    document.getElementById("replyBox").value = data.reply;
}

// Compose Mail
function openGmailCompose() {
    const reply = document.getElementById("replyBox").value;

    if (!reply) {
        alert("Generate a reply first!");
        return;
    }

    // Extract email from sender string
    const senderText = document.getElementById("sender").innerText;

    // Example: "John Doe <john@gmail.com>"
    const emailMatch = senderText.match(/<(.+?)>/);

    let email = "";
    if (emailMatch) {
        email = emailMatch[1];
    } else {
        email = senderText; // fallback
    }

    const subject = document.getElementById("subject").innerText;

    // Encode everything for URL
    const encodedSubject = encodeURIComponent("Re: " + subject);
    const encodedBody = encodeURIComponent(reply);

    const url = `https://mail.google.com/mail/?view=cm&fs=1&to=${email}&su=${encodedSubject}&body=${encodedBody}`;

    window.open(url, "_blank");
}

// History
async function loadHistory() {
    const res = await fetch("/history");
    const data = await res.json();

    const container = document.getElementById("historyList");
    container.innerHTML = "<h3>History</h3>";

    data.forEach(h => {
        const div = document.createElement("div");
        div.className = "email-item";

        div.innerHTML = `
            <strong>Email ID:</strong> ${h.email_id}<br>
            ${h.reply}
        `;

        container.appendChild(div);
    });
}

// Navigation
function goHistory() {
    window.location.href = "/history-page";
}

function goInbox() {
    window.location.href = "/";
}

function logout() {
    document.cookie = "logged_in=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = "/login";
}

// Auto load
// window.onload = loadInbox;
window.onload = () => {
    checkLogin();
    loadInbox();
};