# 📧 AI-Driven Email Classification & Response System

## 🚀 Overview

The **AI-Driven Email Classification & Response System** is a full-stack web application that integrates with Gmail to intelligently manage emails. It allows users to read unread emails, classify them using AI, generate professional replies, and manage handled emails efficiently.

The application uses FastAPI as the backend, PostgreSQL as the database, and integrates with Gmail API using OAuth 2.0. It also includes a modern frontend built with HTML, CSS, JavaScript, and Jinja2 templates.

---

## ✨ Features

* Gmail Authentication using OAuth 2.0
* Fetch unread emails from Gmail
* AI-based email classification:
    * Spam
    * Work
    * Personal
    * Important
* AI reply generation (via API)
* Custom reply generation based on user instruction
* Gmail compose integration (pre-filled email)
* Inbox filtering by category
* Sent/Handled emails section
* Reply history tracking
* Clean modern UI with animations
* Landing page with typing effect and animations
* Loading animations for better UX
* Disabled state for actions on handled emails

## 🏗️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Gmail API (OAuth 2.0)
* HuggingFace Transformers (for classification)
* External API (for reply generation)

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

### Deployment Target

* Render (Free Tier)

---

## 📁 Project Structure

```
ai-email-assistant/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── email.py
│   │   └── reply_history.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── email_routes.py
│   │   └── history_routes.py
│   │
│   ├── services/
│   │   ├── gmail_service.py
│   │   ├── ai_classifier.py
│   │   └── ai_reply_generator.py
│   │
│   ├── templates/
│   │   ├── landing.html
│   │   ├── inbox.html
│   │   └── history.html
│   │
│   └── static/
│       ├── style.css
│       └── script.js
│
├── .env
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd ai-email-assistant
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

Create a `.env` file in root directory:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/email_ai_db
SECRET_KEY=your_secret_key
APP_ENV=development

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

---

### 5️⃣ Database Setup

1. Create PostgreSQL database:

```sql
CREATE DATABASE email_ai_db;
```

2. Tables will be auto-created via SQLAlchemy (if configured).

If needed:

```sql
ALTER TABLE emails ADD COLUMN is_handled BOOLEAN DEFAULT FALSE;
```

## ▶️ Run the Project

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 🧠 Application Workflow

1. User opens landing page
2. Clicks "Login with Gmail"
3. OAuth authentication via Google
4. Redirect to inbox
5. Backend:

   * Fetches unread emails from Gmail
   * Stores new emails in PostgreSQL
   * Classifies emails (if not already classified)
6. User actions:

   * View email content
   * Generate AI reply
   * Generate custom reply
   * Open Gmail compose with pre-filled content
7. After sending:

   * Email marked as handled
   * Removed from inbox
   * Appears in "Sent" section
8. Reply history stored and accessible

---

## 📌 Example Output

### Unread Emails API

```
GET /emails/unread
```

Response:

```json
[
  {
    "id": "19d334999e4e3664",
    "sender": "John Doe <john@example.com>",
    "subject": "Meeting Tomorrow",
    "snippet": "Can we schedule a meeting...",
    "category": "Work"
  }
]
```

---

### AI Reply Response

```json
{
  "reply": "Dear John,\n\nThank you for your email..."
}
```

## 🔮 Future Improvements

* Background job processing (Celery)
* Real email sending via Gmail API (instead of compose redirect)
* Pagination for inbox
* Search and filtering improvements
* Multi-user support
* Performance optimization (caching)
* UI enhancements (dark mode, animations)
* Deployment automation

---

## 🤝 Contribution

Contributions are welcome.

Steps:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push and create Pull Request

---

## 📜 License

This project is open-source and available under the MIT License.

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!