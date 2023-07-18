from django.shortcuts import render

def index(request):
    full_or_widget = request.GET.get('full_or_widget', '').strip()
    gene_uniquename = request.GET.get('gene_uniquename', '').strip()

    context = {
        'full_or_widget': full_or_widget,
        'gene_uniquename': gene_uniquename
    }

    return render(request, 'protein_feature_view/index.html', context)
