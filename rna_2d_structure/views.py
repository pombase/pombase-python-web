from django.shortcuts import render

def index(request):
    gene_uniquename = request.GET.get('gene_uniquename', '').strip()
    urs_id = request.GET.get('urs_id', '').strip()

    context = {
        'gene_uniquename': gene_uniquename,
        'urs_id': urs_id
    }

    return render(request, 'rna_2d_structure/index.html', context)
