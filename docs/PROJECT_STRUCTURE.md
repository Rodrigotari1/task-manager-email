# Project Structure

This document outlines the proper directory structure for all three services in the Task Manager system.

## 1. Email Service (`task-manager-email/`)
Current directory. Handles email notifications.
```
task-manager-email/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── email.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── gmail.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── email.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── email.py
│   ├── templates/
│   │   └── email_templates/
│   │       └── task_notification.html
│   ├── utils/
│   │   ├── __init__.py
│   │   └── email.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_email.py
├── .env
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── Dockerfile
├── README.md
├── credentials.json
├── get_refresh_token.py
├── requirements.txt
└── token.pickle
```

## 2. Main Backend (`task-manager-api/`)
Core service handling tasks and business logic.
```
task-manager-api/
├── api/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── email.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## 3. Frontend (`task-manager-frontend/`)
Streamlit application for user interface.
```
task-manager-frontend/
├── app/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── task_form.py
│   │   └── task_list.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── api.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatting.py
│   ├── __init__.py
│   └── main.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Moving Files to Correct Locations

For the email service (current directory), files are mostly in their correct places. Just ensure:

1. Move `test_email.py` to `tests/test_email.py`
2. Keep configuration files in root:
   - `.env`
   - `.env.example`
   - `credentials.json`
   - `token.pickle`
   - `requirements.txt`
   - `Dockerfile`
   - `README.md`
   - `ARCHITECTURE.md`

## Creating New Services

When creating the other services:

1. Create new directories:
   ```bash
   mkdir -p ../task-manager-api
   mkdir -p ../task-manager-frontend
   ```

2. Initialize each with basic structure:
   ```bash
   # For each service
   mkdir -p {api,tests}/
   touch {api,tests}/__init__.py
   cp .env.example .env
   cp .gitignore .
   ```

3. Copy relevant configuration files:
   - `requirements.txt` (with service-specific dependencies)
   - `Dockerfile`
   - `README.md` 