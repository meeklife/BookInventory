from django.urls import path, re_path
from . import views
from . import api_views
from .views import BookListView

urlpatterns = [
    path('index/', BookListView.as_view(), name='home'),
    path('api/create', api_views.create_book, name='create_book'),
    path('api/delete/<int:book_id>', api_views.delete_book, name='delete_book'),
    path('api/view/<int:book_id>', api_views.view_book, name='view_book'),
    path('api/update/<int:book_id>', api_views.update_book, name='update_book'),
    re_path('login', api_views.login),
    re_path('signup', api_views.signup),
    re_path('test_token', api_views.test_token),
    path('api/checkout/<int:book_id>', views.checkOut, name='checkOut'),
]
