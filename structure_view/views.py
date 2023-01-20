from django.shortcuts import render

def index(request):
    protein_id = request.GET.get('protein_id', '').strip()

    context = {
        'protein_id': protein_id
    }
    return render(request, 'structure_view/index.html', context)

