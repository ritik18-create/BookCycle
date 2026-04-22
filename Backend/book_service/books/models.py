from django.db import models

# Create your models here.
from datetime import datetime

def book_serializer(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "price": book["price"],
        "type": book["type"],  # buy/sell/donate
        "description": book.get("description", ""),
         "image": book.get("image", ""), 
        "created_at": book["created_at"],
        "status": "available"
    }

def create_book(data, user_id):
    return {
        "title": data["title"],
        "author": data["author"],
        "price": data.get("price", 0),
        "image": data.get("image", ""),
        "type": data["type"],
        "description": data.get("description", ""),
        "user_id": user_id,  # ✅ important
        "created_at": datetime.utcnow()
    }