from django.shortcuts import render

def index(request):
    protein_id = request.GET.get('protein_id', '').strip()
    structure_type = request.GET.get('structure_type', '').strip()

    context = {
        'protein_id': protein_id
    }
    if structure_type == 'alphafold':
        return render(request, 'structure_view/index.html', context)
    else:
        return render(request, 'structure_view/pdb_index.html', context)
