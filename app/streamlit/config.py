class Config:
    # API endpoints
    EMAIL_SERVICE_URL = "http://localhost:8002"
    TASK_SERVICE_URL = "http://localhost:8002"
    
    # Task priorities
    TASK_PRIORITIES = {
        1: "Low",
        2: "Medium",
        3: "High"
    }
    
    # Task statuses
    TASK_STATUSES = [
        "pending",
        "email_sent",
        "completed",
        "failed"
    ] 