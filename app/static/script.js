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