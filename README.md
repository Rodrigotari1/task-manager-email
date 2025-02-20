# Task Manager Email Service

A microservice for handling email notifications in the Task Manager application.

## Features

- Send task notification emails via Gmail API
- HTML email templates with Jinja2
- FastAPI REST endpoints
- OAuth2 authentication with Gmail
- Comprehensive error handling and logging

## Prerequisites

- Python 3.12+
- Gmail API credentials
- A Gmail account with API access enabled

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd task-manager-email
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Gmail API:
   - Go to Google Cloud Console
   - Create a project and enable Gmail API
   - Create OAuth2 credentials
   - Download credentials and save as `credentials.json` in the `credentials/` directory

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Gmail API credentials and other settings

## Running the Service

Start the service:
```bash
uvicorn app.main:app --port 8002 --reload
```

The service will be available at `http://localhost:8002`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

## Usage Example

Send a task notification:
```python
import requests

response = requests.post(
    "http://localhost:8002/api/v1/email/send",
    json={
        "to": "recipient@email.com",
        "subject": "New Task",
        "task_id": "123",
        "task_title": "Important Task",
        "task_description": "Please complete this task",
        "priority": 1
    }
)
print(response.json())
```

## Email Tracking

The service includes a script to check email tracking status:

```bash
# Show overall analytics
./scripts/check_tracking.sh

# Check specific email tracking events
./scripts/check_tracking.sh <tracking_id>
```

Example output for analytics:
```
Email Analytics Summary:
====================
Total Sent: 1
Total Opened: 1
Total Clicked: 0
Open Rate: 0.0%
Click Rate: 0.0%
Delivery Rate: 100.0%
```

Example output for specific email:
```
Email Tracking Events for <tracking_id>:
==================
Event: PENDING
Time: 2025-02-20T18:01:39.891637
User Agent: N/A
IP: N/A
Metadata:
  task_id: test123
-------------------
Event: SENT
Time: 2025-02-20T18:01:40.499070
User Agent: N/A
IP: N/A
Metadata:
  message_id: 1952485c806137a7
-------------------
```

## Architecture

See [Architecture Documentation](docs/architecture.md) for detailed information about:
- Component structure
- Flow diagrams
- Authentication
- Security considerations

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Check code style:
```bash
flake8
black .
```

## Security Notes

- Never commit `.env` or credential files
- Keep `credentials/` directory contents secure
- Regularly rotate OAuth2 refresh tokens
- Monitor Gmail API usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[License Type] - See LICENSE file for details 