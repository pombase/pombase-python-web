from django.shortcuts import render

def index(request):
    id = request.GET.get('id', '').strip()
    structure_type = request.GET.get('structure_type', '').strip()

    if structure_type == 'alphafold':
        url = f'https://alphafold.ebi.ac.uk/files/AF-{id}-F1-model_v6.cif'
    else:
        url = f'https://www.ebi.ac.uk/pdbe/model-server/v1/{id}/full?encoding=cif'

    context = {
        'url': url
    }

    return render(request, 'structure_view/index.html', context)
