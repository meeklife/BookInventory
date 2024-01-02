from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from .models import Books
from .serializer import BookSerializer
from rest_framework.decorators import api_view


class BookListView(APIView):
    def get(self, request, *args, **kwargs):
        all_books = Books.objects.all().order_by('id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_books, 6)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        serializer = BookSerializer(page_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def checkOut(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        book.aval_quantity = book.total_quantity - 1
        serializer = BookSerializer(book)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            Response(serializer.errors, status=400)
