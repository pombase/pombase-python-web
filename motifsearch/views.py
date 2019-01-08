import os

from django.shortcuts import render
from django.http import JsonResponse

from motifsearch.search import Search

search = None

def index(request):
    if search == None:
        search = Search(os.environ['PEPTIDE_PATH'])

    data = {
        'key1': 'data1'
    }
    return JsonResponse(data)
