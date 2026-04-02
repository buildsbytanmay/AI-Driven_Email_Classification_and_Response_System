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

## Environment Variables

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

## Database Setup

1. Create PostgreSQL database:

```sql
CREATE DATABASE email_ai_db;
```

2. Tables will be auto-created via SQLAlchemy (if configured).

If needed:

```sql
ALTER TABLE emails ADD COLUMN is_handled BOOLEAN DEFAULT FALSE;
```
