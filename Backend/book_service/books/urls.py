from django.urls import path
from .views import add_book, get_books, delete_book, search_books,buy_book

urlpatterns = [
    path('add/', add_book),
    path('', get_books),
    path('delete/<str:id>/', delete_book),
    path('search/', search_books),
    path("buy/<str:id>/", buy_book), 
#     path(
#     "buy/<str:book_id>/",
#     buy_book
# ),
]