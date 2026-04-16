function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
}

function checkLogin() {
    if (!document.cookie.includes("logged_in=true")) {
        window.location.href = "/login";
    }
}

let currentEmailId = null;

function cleanText(text) {
    if (!text) return "";
    return text.replace(/<[^>]*>/g, "").trim();
}

function badgeClass(cat) {
    const map = { Work: "badge-work", Personal: "badge-personal", Important: "badge-important", Spam: "badge-spam" };
    return map[cat] || "badge-default";
}

function buildEmailCard(email) {
    const cat = email.category || "";
    return `
        <div class="email-item-top">
            <span class="email-item-sender">${email.sender}</span>
            ${cat ? `<span class="badge ${badgeClass(cat)}">${cat}</span>` : ""}
        </div>
        <div class="email-item-subject">${email.subject}</div>
        <div class="email-item-snippet">${cleanText(email.snippet)}</div>
    `;
}

function renderEmailList(data, list) {
    data.forEach(email => {
        const div = document.createElement("div");
        div.className = "email-item";
        div.setAttribute("data-id", email.id);
        div.innerHTML = buildEmailCard(email);
        div.onclick = () => openEmail(email.id);
        list.appendChild(div);
    });
}

// Load Inbox
async function loadInbox() {
    showLoader();
    const res = await fetch("/emails/unread");
    const data = await res.json();
    const list = document.getElementById("emailList");
    list.innerHTML = "";
    if (!data.length) {
        list.innerHTML = `<div class="empty-state"><div class="empty-icon">📭</div><p>No unread emails.</p></div>`;
    } else {
        renderEmailList(data, list);
    }
    hideLoader();
}

// Filter Emails
async function filterEmails(category) {
    showLoader();
    const res = await fetch(`/emails/unread?category=${category}`);
    const data = await res.json();
    const list = document.getElementById("emailList");
    list.innerHTML = "";
    if (!data.length) {
        list.innerHTML = `<div class="empty-state"><div class="empty-icon">📭</div><p>No emails in ${category}.</p></div>`;
    } else {
        renderEmailList(data, list);
    }
    hideLoader();
}

// Open Email
async function openEmail(id) {
    showLoader();
    currentEmailId = id;

    // Highlight selected card
    document.querySelectorAll(".email-item").forEach(el => el.classList.remove("selected"));
    const selected = document.querySelector(`.email-item[data-id="${id}"]`);
    if (selected) selected.classList.add("selected");

    const res = await fetch(`/emails/${id}`);
    const data = await res.json();

    document.getElementById("sender").innerText = data.sender || "";
    document.getElementById("subject").innerText = data.subject || "";
    document.getElementById("body").innerText = data.body;

    const replyBox = document.getElementById("replyBox");
    const isHandled = data.is_handled;

    replyBox.value = isHandled ? (data.reply || "") : "";
    document.getElementById("generateBtn").disabled = isHandled;
    document.getElementById("customBtn").disabled = isHandled;
    document.getElementById("sendBtn").disabled = isHandled;

    hideLoader();
}

// Generate AI Reply
async function generateReply() {
    showLoader();
    const res = await fetch(`/emails/${currentEmailId}/generate-reply`, { method: "POST" });
    const data = await res.json();
    document.getElementById("replyBox").value = data.reply;
    hideLoader();
}

// Custom Reply
async function customReply() {
    showLoader();
    const instruction = document.getElementById("customInput").value;
    const res = await fetch(`/emails/${currentEmailId}/custom-reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ instruction })
    });
    const data = await res.json();
    document.getElementById("replyBox").value = data.reply;
    hideLoader();
}

function removeEmailFromUI(id) {
    const item = document.querySelector(`.email-item[data-id="${id}"]`);
    if (item) item.remove();
}

// Compose Mail
function openGmailCompose() {
    const reply = document.getElementById("replyBox").value;
    if (!reply) { alert("Generate a reply first!"); return; }

    const senderText = document.getElementById("sender").innerText;
    const emailMatch = senderText.match(/<(.+?)>/);
    const email = emailMatch ? emailMatch[1] : senderText;
    const subject = document.getElementById("subject").innerText;

    const url = `https://mail.google.com/mail/?view=cm&fs=1&to=${email}&su=${encodeURIComponent("Re: " + subject)}&body=${encodeURIComponent(reply)}`;
    window.open(url, "_blank");

    removeEmailFromUI(currentEmailId);
    fetch(`/emails/${currentEmailId}/mark-handled`, { method: "POST" });
}

// Load Sent Emails
async function loadSentEmails() {
    showLoader();
    const res = await fetch("/emails/sent");
    const data = await res.json();
    const list = document.getElementById("emailList");
    list.innerHTML = "";
    if (!data.length) {
        list.innerHTML = `<div class="empty-state"><div class="empty-icon">📤</div><p>No sent emails.</p></div>`;
    } else {
        renderEmailList(data, list);
    }
    hideLoader();
}

// History
async function loadHistory() {
    const res = await fetch("/history");
    const data = await res.json();
    const container = document.getElementById("historyList");
    container.innerHTML = "<h3>🕘 Reply History</h3>";

    if (!data.length) {
        container.innerHTML += `<div class="empty-state"><div class="empty-icon">📋</div><p>No reply history yet.</p></div>`;
        return;
    }

    data.forEach(h => {
        const card = document.createElement("div");
        card.className = "history-card";
        card.innerHTML = `<strong>Email ID: ${h.email_id}</strong><p>${h.reply}</p>`;
        container.appendChild(card);
    });
}

// Navigation
function goHistory() { window.location.href = "/history-page"; }
function goInbox()   { window.location.href = "/inbox"; }
function logout() {
    document.cookie = "logged_in=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = "/";
}

window.onload = () => {
    checkLogin();
    loadInbox();
};
