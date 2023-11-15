from django.shortcuts import render, redirect, get_object_or_404
from .models import Books
from rest_framework.response import Response
from .serializer import BookSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    if request.method == 'POST':
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
def delete_book(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        book.delete()
        return Response(status=204)
    else:
        return Response("Book not found", status=404)


@api_view(['GET'])
def view_book(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
def update_book(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        data = request.data
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response('Books not found', status=404)


# Creating Users and User Authentication

@api_view(['POST'])
def login(request):
    print(request.data)
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=400)
