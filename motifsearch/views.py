import os

from django.shortcuts import render
from django.http import JsonResponse

from motifsearch.search import Search

search = None

def query(request, pattern):
    global search
    if search == None:
        search = Search(os.environ['PEPTIDE_PATH'])

    return JsonResponse({
        'status': 'OK',
        'peptide_matches': search.motif(pattern)
    })
