from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from .mongo import books_collection
from .models import create_book, book_serializer

from bson import ObjectId
import jwt


# ==========================================
# 🔐 JWT AUTH FUNCTION
# ==========================================

def get_user_from_token(request):

    auth_header = request.headers.get("Authorization")

    print("AUTH HEADER:", auth_header)

    if not auth_header:
        return None

    try:
        # Extract token
        token = auth_header.split(" ")[1]

        print("TOKEN:", token)

        # Decode JWT
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        print("JWT VERIFIED:", decoded_token)

        return decoded_token["user_id"]

    except Exception as e:
        print("JWT ERROR:", str(e))
        return None


# ==========================================
# ➕ ADD BOOK
# ==========================================

@api_view(["POST"])
def add_book(request):

    user_id = get_user_from_token(request)

    if not user_id:
        return Response(
            {"error": "Invalid or missing token"},
            status=401
        )

    data = request.data

    required_fields = ["title", "author", "type"]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"{field} is required"},
                status=400
            )

    # Create book
    book = create_book(data, user_id)

    result = books_collection.insert_one(book)

    book["_id"] = result.inserted_id

    return Response({
        "message": "Book added successfully ✅",
        "book": book_serializer(book)
    })


# ==========================================
# 📚 GET ALL BOOKS
# ==========================================

@api_view(["GET"])
def get_books(request):

    books = books_collection.find().sort("created_at", -1)

    return Response([
        book_serializer(book)
        for book in books
    ])


# ==========================================
# ❌ DELETE BOOK
# ==========================================

@api_view(["DELETE"])
def delete_book(request, id):

    user_id = get_user_from_token(request)

    if not user_id:
        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    try:
        book = books_collection.find_one({
            "_id": ObjectId(id)
        })

    except Exception:
        return Response(
            {"error": "Invalid Book ID"},
            status=400
        )

    # Book not found
    if not book:
        return Response(
            {"error": "Book not found"},
            status=404
        )

    # Ownership check
    if str(book.get("user_id")) != str(user_id):
        return Response(
            {"error": "You are not allowed to delete this book"},
            status=403
        )

    # Delete book
    books_collection.delete_one({
        "_id": ObjectId(id)
    })

    return Response({
        "message": "Book deleted successfully ✅"
    })


# ==========================================
# 🛒 BUY BOOK
# ==========================================

@api_view(["POST"])
def buy_book(request, id):

    user_id = get_user_from_token(request)

    if not user_id:
        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    try:
        book = books_collection.find_one({
            "_id": ObjectId(id)
        })

    except Exception:
        return Response(
            {"error": "Invalid Book ID"},
            status=400
        )

    # Book not found
    if not book:
        return Response(
            {"error": "Book not found"},
            status=404
        )

    # Cannot buy own book
    if str(book.get("user_id")) == str(user_id):
        return Response(
            {"error": "You cannot buy your own book"},
            status=400
        )

    # Already sold
    if book.get("status") == "sold":
        return Response(
            {"error": "Book already sold"},
            status=400
        )

    # Mark as sold
    books_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "sold"
            }
        }
    )

    return Response({
        "message": "Book purchased successfully ✅"
    })


# ==========================================
# 🔍 SEARCH BOOKS
# ==========================================

@api_view(["GET"])
def search_books(request):

    query = request.GET.get("q", "")

    books = books_collection.find({
        "$or": [
            {
                "title": {
                    "$regex": query,
                    "$options": "i"
                }
            },
            {
                "author": {
                    "$regex": query,
                    "$options": "i"
                }
            },
        ]
    })

    return Response([
        book_serializer(book)
        for book in books
    ])