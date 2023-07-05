from django.shortcuts import render

def index(request):
    gene_uniquename = request.GET.get('gene_uniquename', '').strip()

    context = {
        'gene_uniquename': gene_uniquename
    }

    return render(request, 'protein_feature_view/index.html', context)
