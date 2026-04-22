from rest_framework.decorators import api_view
from rest_framework.response import Response
from .mongo import users_collection
from .models import create_user, user_serializer
from django.contrib.auth.hashers import make_password, check_password
from .utils import generate_token


@api_view(['POST'])
def register(request):
    data = request.data
    print("DATA RECEIVED:", data)

    # Check if user exists
    if users_collection.find_one({"email": data["email"]}):
        return Response({"error": "User already exists"}, status=400)

    # Hash password
    hashed_password = make_password(data["password"])

    user = create_user(data["name"], data["email"], hashed_password)

    result = users_collection.insert_one(user)
    user["_id"] = result.inserted_id

    token = generate_token(user)

    return Response({
        "message": "User registered successfully",
        "token": token,
        "user": user_serializer(user)
    })


@api_view(['POST'])
def login(request):
    data = request.data

    # Validate input
    if "email" not in data or "password" not in data:
        return Response({"error": "Email and password required"}, status=400)

    user = users_collection.find_one({"email": data["email"]})

    if not user:
        return Response({"error": "User not found"}, status=404)

    if not check_password(data["password"], user["password"]):
        return Response({"error": "Invalid password"}, status=400)

    token = generate_token(user)

    return Response({
        "message": "Login successful",
        "token": token,
        "user": user_serializer(user)
    })