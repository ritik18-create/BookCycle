from django.db import models

# Create your models here.
from datetime import datetime

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }

def create_user(name, email, password):
    return {
        "name": name,
        "email": email,
        "password": password,
        "created_at": datetime.utcnow()
    }