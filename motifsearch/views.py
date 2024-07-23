import os

from django.http import JsonResponse

from motifsearch.search import Search

search = None

def query(request):
    global search
    if search is None:
        search = Search(os.environ['PEPTIDE_PATH'])

    scope = request.GET.get('scope', '').strip()
    pattern = request.GET.get('pattern', '').strip()
    max_gene_details = request.GET.get('max_gene_details')

    if max_gene_details.isdigit():
        max_gene_details = int(max_gene_details)
    else:
        if max_gene_details == 'all':
            max_gene_details = -1
        else:
            max_gene_details = 500

    if len(pattern) < 1:
        return JsonResponse({
            'status': 'error',
            'message': 'pattern too short'
        })

    return JsonResponse({
        'status': 'OK',
        'peptide_matches': search.motif(scope, pattern, max_gene_details = max_gene_details)
    })

def ping(request):
    return JsonResponse({ 'status': 'OK' })
