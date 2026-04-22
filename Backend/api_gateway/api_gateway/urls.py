"""
URL configuration for api_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    proxy_register,
    proxy_login,
    proxy_add_book,
    proxy_get_books,
    proxy_delete_book,
    proxy_search_books
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/register/', proxy_register),
    path('api/auth/login/', proxy_login),

    # Books
    path('api/books/add/', proxy_add_book),
    path('api/books/', proxy_get_books),
    path('api/books/delete/<str:id>/', proxy_delete_book),
    path('api/books/search/', proxy_search_books),
]
