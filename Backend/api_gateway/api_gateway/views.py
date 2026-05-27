import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response


# ==========================================
# 🔗 MICROSERVICE URLS
# ==========================================

AUTH_SERVICE = "http://127.0.0.1:8001"
BOOK_SERVICE = "http://127.0.0.1:8002"


# ==========================================
# 🔐 AUTH ROUTES
# ==========================================

@api_view(["POST"])
def proxy_register(request):

    response = requests.post(
        f"{AUTH_SERVICE}/api/auth/register/",
        json=request.data
    )

    return Response(
        response.json(),
        status=response.status_code
    )


@api_view(["POST"])
def proxy_login(request):

    response = requests.post(
        f"{AUTH_SERVICE}/api/auth/login/",
        json=request.data
    )

    return Response(
        response.json(),
        status=response.status_code
    )


# ==========================================
# 📚 GET ALL BOOKS
# ==========================================

@api_view(["GET"])
def proxy_get_books(request):

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    print("FORWARDED AUTH HEADER:", headers)

    response = requests.get(
        f"{BOOK_SERVICE}/api/books/",
        headers=headers
    )

    return Response(
        response.json(),
        status=response.status_code
    )


# ==========================================
# ➕ ADD BOOK
# ==========================================

@api_view(["POST"])
def proxy_add_book(request):

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    print("FORWARDED AUTH HEADER:", headers)

    response = requests.post(
        f"{BOOK_SERVICE}/api/books/add/",
        headers=headers,
        json=request.data
    )

    return Response(
        response.json(),
        status=response.status_code
    )


# ==========================================
# ❌ DELETE BOOK
# ==========================================

@api_view(["DELETE"])
def proxy_delete_book(request, id):

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    print("FORWARDED AUTH HEADER:", headers)

    response = requests.delete(
        f"{BOOK_SERVICE}/api/books/delete/{id}/",
        headers=headers
    )

    return Response(
        response.json(),
        status=response.status_code
    )


# ==========================================
# 🛒 BUY BOOK
# ==========================================

@api_view(["POST"])
def proxy_buy_book(request, id):

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    print("FORWARDED AUTH HEADER:", headers)

    response = requests.post(
        f"{BOOK_SERVICE}/api/books/buy/{id}/",
        headers=headers
    )

    return Response(
        response.json(),
        status=response.status_code
    )


# ==========================================
# 🔍 SEARCH BOOKS
# ==========================================

@api_view(["GET"])
def proxy_search_books(request):

    query = request.GET.get("q", "")

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    print("FORWARDED AUTH HEADER:", headers)

    response = requests.get(
        f"{BOOK_SERVICE}/api/books/search/?q={query}",
        headers=headers
    )

    return Response(
        response.json(),
        status=response.status_code
    )