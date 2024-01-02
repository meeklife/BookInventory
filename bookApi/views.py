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


@api_view(['POST'])
def checkOut(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    if book:
        if book.aval_quantity > 0:
            book.aval_quantity -= 1
            book.save()
            return Response({"message": "Book checked out successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Book copy isn't available for checkout"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
