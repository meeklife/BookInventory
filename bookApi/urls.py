from django.urls import path, re_path
from rest_framework import permissions
from . import views
from . import api_views
from .views import BookListView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs for Book Inventory",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('index/', BookListView.as_view(), name='home'),
    path('api/create', api_views.create_book, name='create_book'),
    path('api/delete/<int:book_id>', api_views.delete_book, name='delete_book'),
    path('api/view/<int:book_id>', api_views.view_book, name='view_book'),
    path('api/update/<int:book_id>', api_views.update_book, name='update_book'),
    re_path('login', api_views.login),
    re_path('signup', api_views.signup),
    path('api/checkout/<int:book_id>', views.checkOut, name='checkOut'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
