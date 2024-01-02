from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Books

from rest_framework.response import Response
from .serializer import BookSerializer, UserSerializer, LoginSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='POST', request_body=BookSerializer)
@api_view(['POST'])
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
    else:
        return Response('Book not found', status=404)


@swagger_auto_schema(method='PATCH', request_body=BookSerializer)
@api_view(['PATCH'])
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

@swagger_auto_schema(method='POST', request_body=LoginSerializer)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@swagger_auto_schema(method='POST', request_body=UserSerializer)
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
