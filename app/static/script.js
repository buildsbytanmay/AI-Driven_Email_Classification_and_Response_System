function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
}

function checkLogin() {
    const loggedIn = document.cookie.includes("logged_in=true");

    if (!loggedIn) {
        window.location.href = "/login";
    }
}

let currentEmailId = null;

// Clean text
function cleanText(text) {
    if (!text) return "";

    // Remove HTML tags
    return text.replace(/<[^>]*>/g, "").trim();
}


// Load Inbox
async function loadInbox() {
    showLoader();

    const res = await fetch("/emails/unread");
    const data = await res.json();

    const list = document.getElementById("emailList");
    list.innerHTML = "<h3>Inbox</h3>";

    data.forEach(email => {
        const div = document.createElement("div");
        div.className = "email-item";
        div.setAttribute("data-id", email.id);

        div.innerHTML = `
    <strong>${email.sender}</strong>
    <span style="
        float:right;
        font-size:11px;
        background:#dbeafe;
        color:#1d4ed8;
        padding:3px 6px;
        border-radius:6px;
    ">
        ${email.category || ""}
    </span><br>
    ${email.subject}<br>
    <small>${cleanText(email.snippet)}</small>
`;

        div.onclick = () => openEmail(email.id);

        list.appendChild(div);
    });

    hideLoader();
}


// Filter Emails
async function filterEmails(category) {
    showLoader();

    const res = await fetch(`/emails/unread?category=${category}`);
    const data = await res.json();

    const list = document.getElementById("emailList");
    list.innerHTML = `<h3>${category}</h3>`;

    data.forEach(email => {
        const div = document.createElement("div");
        div.className = "email-item";
        div.setAttribute("data-id", email.id);

        div.innerHTML = `
    <strong>${email.sender}</strong>
    <span style="
        float:right;
        font-size:11px;
        background:#dbeafe;
        color:#1d4ed8;
        padding:3px 6px;
        border-radius:6px;
    ">
        ${email.category || ""}
    </span><br>
    ${email.subject}<br>
    <small>${cleanText(email.snippet)}</small>
`;

        div.onclick = () => openEmail(email.id);

        list.appendChild(div);
    });

    hideLoader();
}


// Open Email
async function openEmail(id) {
    showLoader();

    currentEmailId = id;

    const res = await fetch(`/emails/${id}`);
    const data = await res.json();

    document.getElementById("sender").innerText = data.sender || "";
    document.getElementById("subject").innerText = data.subject || "";
    document.getElementById("body").innerText = data.body;

    const replyBox = document.getElementById("replyBox");

    // 🔥 If email is from SENT
    if (data.is_handled) {
        replyBox.value = data.reply || "";

        // ❌ Disable buttons
        document.getElementById("generateBtn").disabled = true;
        document.getElementById("customBtn").disabled = true;
        document.getElementById("sendBtn").disabled = true;

    } else {
        // Inbox email

        replyBox.value = "";

        // ✅ Enable buttons
        document.getElementById("generateBtn").disabled = false;
        document.getElementById("customBtn").disabled = false;
        document.getElementById("sendBtn").disabled = false;
    }

    hideLoader();
}

// Generate AI Reply
async function generateReply() {
    showLoader();

    const res = await fetch(`/emails/${currentEmailId}/generate-reply`, {
        method: "POST"
    });

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
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ instruction })
    });

    const data = await res.json();

    document.getElementById("replyBox").value = data.reply;

    hideLoader();
}


function removeEmailFromUI(id) {
    const items = document.querySelectorAll(".email-item");

    items.forEach(item => {
        if (item.getAttribute("data-id") === id) {
            item.remove();
        }
    });
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

    // 🔥 REMOVE EMAIL FROM UI
    removeEmailFromUI(currentEmailId);

    fetch(`/emails/${currentEmailId}/mark-handled`, {
        method: "POST"
    });
}

// Load sent emails
async function loadSentEmails() {
    showLoader();

    const res = await fetch("/emails/sent");
    const data = await res.json();

    const list = document.getElementById("emailList");
    list.innerHTML = "<h3>Sent Emails</h3>";

    // data.forEach(email => {
    //     const div = document.createElement("div");
    //     div.className = "email-item";
    //     div.setAttribute("data-id", email.id);

    //     div.innerHTML = `
    //         <strong>${email.sender}</strong><br>
    //         ${email.subject}<br>
    //         <small>${cleanText(email.snippet)}</small>
    //     `;

    //     list.appendChild(div);
    data.forEach(email => {
    const div = document.createElement("div");
    div.className = "email-item";
    div.setAttribute("data-id", email.id);

    div.innerHTML = `
        <strong>${email.sender}</strong>
        <span style="
            float:right;
            font-size:11px;
            background:#dbeafe;
            color:#1d4ed8;
            padding:3px 6px;
            border-radius:6px;
        ">
            ${email.category || ""}
        </span><br>
        ${email.subject}<br>
        <small>${cleanText(email.snippet)}</small>
    `;

    // 🔥 THIS LINE IS MISSING
    div.onclick = () => openEmail(email.id);

    list.appendChild(div);
    });

    hideLoader();
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
        div.setAttribute("data-id", email.id);

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