from django.shortcuts import render, HttpResponse
from .models import Books
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from rest_framework.response import Response
from .serializer import BookSerializer
from django.core import serializers
import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound


class BookListView(View):

    def get(self, request, *args, **kwargs):
        all_books = Books.objects.get_queryset().order_by('id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_books, 6)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        my_json = serializers.serialize('json', page_obj)

        return HttpResponse(my_json, content_type='application/json')


def checkOut(request, book_id):
    book = Books.objects.filter(id=book_id).first()
    book.aval_quantity = book.total_quantity - 1
    book.save()
    context = {'book': book}
    return HttpResponse(context)
