from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from bson import ObjectId

from .mongo import books_collection
from .models import create_book, book_serializer



# ==========================================
# 🔐 VERIFY JWT TOKEN
# ==========================================

def verify_token(request):

    auth_header = request.headers.get("Authorization")

    print("AUTH HEADER RECEIVED:", auth_header)

    if not auth_header:
        return None

    try:
        # Extract token
        token = auth_header.split(" ")[1]

        # Decode JWT
        decoded = AccessToken(token)

        print("TOKEN VALID:", decoded)

        return decoded

    except Exception as e:

        print("JWT ERROR:", str(e))

        return None


# ==========================================
# ➕ ADD BOOK
# ==========================================

@api_view(["POST"])
def add_book(request):

    user = verify_token(request)

    if not user:
        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    data = request.data

    required_fields = [
        "title",
        "author",
        "type"
    ]

    for field in required_fields:

        if field not in data:

            return Response(
                {"error": f"{field} is required"},
                status=400
            )

    # Get user id from token
    user_id = user["user_id"]

    # Create book object
    book = create_book(data, user_id)

    # Save book in MongoDB
    result = books_collection.insert_one(book)

    # Add inserted id
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

    user = verify_token(request)

    if not user:

        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    books = books_collection.find().sort(
        "created_at",
        -1
    )

    serialized_books = [
        book_serializer(book)
        for book in books
    ]

    return Response(serialized_books)


# ==========================================
# ❌ DELETE BOOK
# ==========================================

@api_view(["DELETE"])
def delete_book(request, id):

    user = verify_token(request)

    if not user:

        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    user_id = user["user_id"]

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

    user = verify_token(request)

    if not user:

        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    user_id = user["user_id"]

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

    # Prevent buying own book
    if str(book.get("user_id")) == str(user_id):

        return Response(
            {"error": "You cannot buy your own book"},
            status=400
        )

    # Check sold status
    if book.get("status") == "sold":

        return Response(
            {"error": "Book already sold"},
            status=400
        )

    # Update status
    books_collection.update_one(
        {
            "_id": ObjectId(id)
        },
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

    user = verify_token(request)

    if not user:

        return Response(
            {"error": "Unauthorized"},
            status=401
        )

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
            }

        ]
    })

    serialized_books = [
        book_serializer(book)
        for book in books
    ]

    return Response(serialized_books)
# @api_view(["POST"])
# def buy_book(request, book_id):

#     user = verify_token(request)

#     if not user:
#         return Response(
#             {"error":"Unauthorized"},
#             status=401
#         )

#     try:
#         book = Book.objects.get(id=book_id)

#         if getattr(book, "is_sold", False):
#             return Response(
#                 {"message":"Already sold"},
#                 status=400
#             )

#         order = Order.objects.create(
#             book_id=str(book.id),
#             buyer_id=str(user["user_id"]),
#             seller_id=str(book.user_id),
#             status="Success"
#         )

#         book.is_sold = True
#         book.save()

#         return Response({
#             "message":"Purchase successful",
#             "order_id": order.id
#         })

#     except Exception as e:
#         return Response(
#             {"error": str(e)},
#             status=400
#         )