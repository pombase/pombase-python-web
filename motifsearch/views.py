import os

from django.shortcuts import render
from django.http import JsonResponse

from motifsearch.search import Search

search = None

def query(request):
    global search
    if search == None:
        search = Search(os.environ['PEPTIDE_PATH'])

    scope = request.GET.get('scope', '').strip()
    pattern = request.GET.get('pattern', '').strip()

    if len(pattern) < 1:
        return JsonResponse({
            'status': 'error',
            'message': 'pattern too short'
        })

    return JsonResponse({
        'status': 'OK',
        'peptide_matches': search.motif(scope, pattern)
    })

def ping(request):
    return JsonResponse({ 'status': 'OK' })
