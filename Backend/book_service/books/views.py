from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .mongo import books_collection
from .models import create_book, book_serializer
from bson import ObjectId
import jwt
import os
from dotenv import load_dotenv



load_dotenv()
SECRET = os.getenv("JWT_SECRET")
print("BOOK SERVICE SECRET:", SECRET) 


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization")

    print("AUTH HEADER RECEIVED:", auth_header)  # ✅ correct indentation

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded["user_id"]
    except Exception as e:
        print("JWT ERROR:", e)
        return None


# ➕ Add Book
# @api_view(['POST'])
# def add_book(request):
#     data = request.data

#     required_fields = ["title", "author", "type"]

#     for field in required_fields:
#         if field not in data:
#             return Response({"error": f"{field} is required"}, status=400)

#     book = create_book(data)
#     result = books_collection.insert_one(book)
#     book["_id"] = result.inserted_id

#     return Response({
#         "message": "Book added successfully",
#         "book": book_serializer(book)
#     })
@api_view(['POST'])
def add_book(request):
    user_id = get_user_from_token(request)
      
    if not user_id:
        return Response({"error": "Unauthorized"}, status=401)

    data = request.data
    
    book = create_book(data, user_id)

    result = books_collection.insert_one(book)
    book["_id"] = result.inserted_id
    

    return Response({
        "message": "Book added",
        "book": book_serializer(book),
       
    })


# 📚 Get All Books
@api_view(['GET'])
def get_books(request):
    books = books_collection.find().sort("created_at", -1)

    return Response([book_serializer(book) for book in books])


# ❌ Delete Book
# @api_view(['DELETE'])
# def delete_book(request, id):
#     result = books_collection.delete_one({"_id": ObjectId(id)})

#     if result.deleted_count == 0:
#         return Response({"error": "Book not found"}, status=404)

#     return Response({"message": "Book deleted successfully"})
@api_view(['DELETE'])
def delete_book(request, id):
    # 🔐 Get user from JWT
    user_id = get_user_from_token(request)

    if not user_id:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        return Response({"error": "Invalid book ID"}, status=400)

    # ❌ Book not found
    if not book:
        return Response({"error": "Book not found"}, status=404)

    # 🔐 Ownership check (VERY IMPORTANT)
    if str(book.get("user_id")) != str(user_id):
        return Response(
            {"error": "You are not allowed to delete this book"},
            status=403
        )

    # ✅ Delete book
    books_collection.delete_one({"_id": ObjectId(id)})

    return Response({"message": "Book deleted successfully"}, status=200)
@api_view(['POST'])
def buy_book(request, id):
    user_id = get_user_from_token(request)

    if not user_id:
        return Response({"error": "Unauthorized"}, status=401)

    book = books_collection.find_one({"_id": ObjectId(id)})

    if not book:
        return Response({"error": "Book not found"}, status=404)

    # ❌ Cannot buy your own book
    if str(book.get("user_id")) == str(user_id):
        return Response({"error": "You cannot buy your own book"}, status=400)

    # ❌ Already sold
    if book.get("status") == "sold":
        return Response({"error": "Book already sold"}, status=400)

    # ✅ Mark as sold
    books_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "sold"}}
    )

    return Response({"message": "Book purchased successfully"})

# 🔍 Search Books
@api_view(['GET'])
def search_books(request):
    query = request.GET.get("q", "")

    books = books_collection.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}},
        ]
    })

    return Response([book_serializer(book) for book in books])