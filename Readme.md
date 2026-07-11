# 📧 AI-Driven Email Classification & Response System

An AI-powered full-stack web application that integrates with **Gmail** to intelligently manage emails. The system fetches unread emails, classifies them using AI, generates professional replies, and helps users organize handled emails efficiently.

Built with **FastAPI**, **PostgreSQL**, **Gmail API (OAuth 2.0)**, and a modern frontend using **HTML, CSS, JavaScript, and Jinja2 Templates**.

---

## 🚀 Overview

The application allows users to:

- Authenticate securely with Gmail using OAuth 2.0
- Fetch unread emails directly from Gmail
- Automatically classify emails using AI
- Generate professional AI-powered replies
- Create custom replies from user instructions
- Open Gmail Compose with pre-filled responses
- Track handled emails and reply history
- Manage emails through a clean and responsive interface

---

## ✨ Features

### 📬 Email Management

- Gmail Authentication using OAuth 2.0
- Fetch unread emails from Gmail
- Inbox filtering by category
- Sent/Handled emails section
- Reply history tracking

### 🤖 AI Features

- AI-based email classification
  - Spam
  - Work
  - Personal
  - Important
- AI reply generation (via API)
- Custom reply generation based on user instructions

### 🎨 User Experience

- Modern responsive interface
- Landing page with typing animation
- Smooth loading animations
- Gmail compose integration with pre-filled emails
- Disabled actions for already handled emails

---

## 🏗️ Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API development |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| Gmail API | Gmail integration |
| OAuth 2.0 | User authentication |
| HuggingFace Transformers | Email classification |
| External API | AI reply generation |

### Frontend

| Technology | Purpose |
|------------|---------|
| HTML | Page structure |
| CSS | Styling |
| JavaScript | Client-side functionality |
| Jinja2 Templates | Server-side rendering |

### Deployment

| Platform | Usage |
|----------|-------|
| Render (Free Tier) | Application deployment |

---

## 📁 Project Structure

```text
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

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or later
- PostgreSQL
- Gmail API credentials
- Git

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-email-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/email_ai_db
SECRET_KEY=your_secret_key
APP_ENV=development

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

---

### 5. Database Setup

Create the PostgreSQL database.

```sql
CREATE DATABASE email_ai_db;
```

Database tables will be created automatically by SQLAlchemy (if configured).

If required, run:

```sql
ALTER TABLE emails
ADD COLUMN is_handled BOOLEAN DEFAULT FALSE;
```

---

## ▶️ Running the Application

Start the development server.

```bash
uvicorn app.main:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

# 🧠 Application Workflow

```text
Landing Page
      │
      ▼
Login with Gmail
      │
      ▼
Google OAuth Authentication
      │
      ▼
Inbox
      │
      ▼
Fetch Unread Emails
      │
      ▼
Store in PostgreSQL
      │
      ▼
AI Classification
      │
      ▼
User Actions
 ├── View Email
 ├── Generate AI Reply
 ├── Generate Custom Reply
 └── Open Gmail Compose
      │
      ▼
Mark as Handled
      │
      ▼
Reply History
```

---

## 📌 API Example

### Fetch Unread Emails

**Request**

```http
GET /emails/unread
```

**Response**

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

### AI Reply Generation

**Response**

```json
{
  "reply": "Dear John,\n\nThank you for your email..."
}
```

---

# 🔮 Future Improvements

- Background job processing using Celery
- Direct email sending through Gmail API
- Inbox pagination
- Improved search and filtering
- Multi-user support
- Performance optimization through caching
- Additional UI improvements
- Dark mode
- Deployment automation

---

# 🤝 Contributing

Contributions are welcome.

### Fork the Repository

Create your own copy of the project.

### Create a Feature Branch

```bash
git checkout -b feature-name
```

### Commit Your Changes

```bash
git commit -m "Add feature"
```

### Push the Branch

```bash
git push origin feature-name
```

Finally, open a Pull Request.

---

# 📜 License

This project is open-source and available under the **MIT License**.

---

# ⭐ Support

If you found this project helpful, consider giving it a **⭐ Star** on GitHub!
