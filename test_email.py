import requests

# The email service URL
EMAIL_SERVICE_URL = "http://localhost:8002"

# Test data
test_email = {
    "to": "rodrigocarderera@gmail.com",  # Your email
    "subject": "Test Task Created",
    "task_id": "123",
    "task_title": "Test Task",
    "task_description": "This is a test task to verify email notifications are working correctly.",
    "priority": 1  # 1=Highest, 2=High, 3=Medium, 4=Low, 5=Lowest
}

# Send the test email
response = requests.post(
    f"{EMAIL_SERVICE_URL}/api/v1/email/send",
    json=test_email
)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json()) 