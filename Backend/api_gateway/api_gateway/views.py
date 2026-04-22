import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

AUTH_SERVICE = "http://127.0.0.1:8001"
BOOK_SERVICE = "http://127.0.0.1:8002"


# 🔐 AUTH ROUTES
@api_view(['POST'])
def proxy_register(request):
    res = requests.post(f"{AUTH_SERVICE}/api/auth/register/", json=request.data)
    return Response(res.json(), status=res.status_code)


@api_view(['POST'])
def proxy_login(request):
    res = requests.post(f"{AUTH_SERVICE}/api/auth/login/", json=request.data)
    return Response(res.json(), status=res.status_code)


# 📚 BOOK ROUTES
# @api_view(['POST'])
# def proxy_add_book(request):
#     res = requests.post(f"{BOOK_SERVICE}/api/books/add/", json=request.data)
#     return Response(res.json(), status=res.status_code)
@api_view(['POST'])
def proxy_add_book(request):
    headers = {}

    if "Authorization" in request.headers:
        headers["Authorization"] = request.headers["Authorization"]

    res = requests.post(
        f"{BOOK_SERVICE}/api/books/add/",
        json=request.data,
        headers=headers
    )

    return Response(res.json(), status=res.status_code)


# @api_view(['GET'])
# def proxy_get_books(request):
#     res = requests.get(f"{BOOK_SERVICE}/api/books/")
#     return Response(res.json(), status=res.status_code)
@api_view(['GET'])
def proxy_get_books(request):
    headers = {}

    if "Authorization" in request.headers:
        headers["Authorization"] = request.headers["Authorization"]

    res = requests.get(
        f"{BOOK_SERVICE}/api/books/",
        headers=headers
    )

    return Response(res.json(), status=res.status_code)


# @api_view(['DELETE'])
# def proxy_delete_book(request, id):
#     res = requests.delete(f"{BOOK_SERVICE}/api/books/delete/{id}/")
#     return Response(res.json(), status=res.status_code)
@api_view(['DELETE'])
def proxy_delete_book(request, id):
    headers = {}

    if "Authorization" in request.headers:
        headers["Authorization"] = request.headers["Authorization"]

    res = requests.delete(
        f"{BOOK_SERVICE}/api/books/delete/{id}/",
        headers=headers
    )

    return Response(res.json(), status=res.status_code)

@api_view(['GET'])
def proxy_search_books(request):
    query = request.GET.get("q", "")
    res = requests.get(f"{BOOK_SERVICE}/api/books/search/?q={query}")
    return Response(res.json(), status=res.status_code)