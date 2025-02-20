# Task Manager Email Service

A microservice that handles all email communications for the Task Manager application using Gmail API.

## Features

- Send task notification emails
- Track email delivery status
- Beautiful email templates
- Gmail API integration
- Docker support

## Prerequisites

- Python 3.12+
- Gmail API credentials
- Docker (optional)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager-email.git
cd task-manager-email
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up Gmail API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials

4. Create a `.env` file:
```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
EMAIL_SENDER=your@gmail.com
EMAIL_SENDER_NAME="Task Manager"
PORT=8001
ENVIRONMENT=development
```

## Running the Service

### Local Development

```bash
uvicorn app.main:app --reload --port 8001
```

### Docker

1. Build the image:
```bash
docker build -t task-manager-email .
```

2. Run the container:
```bash
docker run -p 8001:8001 --env-file .env task-manager-email
```

## API Endpoints

### Send Email
```http
POST /api/v1/email/send
Content-Type: application/json

{
    "to": "recipient@example.com",
    "subject": "Task: Complete documentation",
    "task_id": "uuid-here",
    "task_title": "Complete documentation",
    "task_description": "Write technical documentation...",
    "priority": 1
}
```

### Get Email Status
```http
GET /api/v1/email/status/{message_id}
```

## Development

### Project Structure
```
task-manager-email/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── email.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── gmail.py
│   │   ├── models/
│   │   │   └── email.py
│   │   ├── services/
│   │   │   └── email.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   └── task_created.html
│   │   └── utils/
│   │   └── template.py
│   ├── tests/
│   ├── .env.example
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
```

### Running Tests
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT 