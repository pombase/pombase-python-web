from django.shortcuts import render

def index(request):
    scope = request.GET.get('scope', '').strip()
    gene_uniquename = request.GET.get('gene_uniquename', '').strip()

    context = {
        'scope': scope,
        'gene_uniquename': gene_uniquename
    }

    return render(request, 'protein_feature_view/index.html', context)
