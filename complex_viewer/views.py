from django.shortcuts import render

def index(request):
    complex_id = request.GET.get('complex_id', '').strip()

    context = {
        'complex_id': complex_id,
    }

    return render(request, 'complex_viewer/index.html', context)
