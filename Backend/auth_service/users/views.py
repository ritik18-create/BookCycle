# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken


# @api_view(['POST'])
# def register(request):
#     username = request.data.get("username")
#     email = request.data.get("email")
#     password = request.data.get("password")

#     # Validate fields
#     if not username or not email or not password:
#         return Response(
#             {"error": "Username, email, and password are required"},
#             status=400
#         )

#     # Check existing username
#     if User.objects.filter(username=username).exists():
#         return Response(
#             {"error": "Username already exists"},
#             status=400
#         )

#     # Check existing email
#     if User.objects.filter(email=email).exists():
#         return Response(
#             {"error": "Email already exists"},
#             status=400
#         )

#     # Create user
#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password
#     )

#     return Response({
#         "message": "User registered successfully",
#         "user": {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email
#         }
#     })


# @api_view(['POST'])
# def login(request):
#     username = request.data.get("email")
#     password = request.data.get("password")
#     print(request.data)

#     # Validate fields
#     if not username or not password:
#         return Response(
#             {"error": "email and password are required"},
#             status=400
#         )

#     # Authenticate user
#     user = authenticate(username=email, password=password)

#     if user is None:
#         return Response(
#             {"error": "Invalid credentials"},
#             status=400
#         )

#     # Generate JWT tokens
#     refresh = RefreshToken.for_user(user)

#     return Response({
#         "message": "Login successful",
#         "refresh": str(refresh),
#         "access": str(refresh.access_token),
#         "user": {
#             "id": user.id,
#             "username": user.email,
#             "email": user.email
#         }
#     })

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    print("REGISTER DATA:", request.data)

    # Validate fields
    if not username or not email or not password:
        return Response(
            {"error": "Username, email, and password are required"},
            status=400
        )

    # Check existing username
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=400
        )

    # Check existing email
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=400
        )

    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })


@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    print("LOGIN DATA:", request.data)

    # Validate fields
    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=400
        )

    # Find user using email
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=404
        )

    # Authenticate using username
    user = authenticate(
        username=user_obj.username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=400
        )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })