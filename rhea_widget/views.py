from django.shortcuts import render

def index(request):
    view_type = request.GET.get('view_type', '').strip()
    rhea_id = request.GET.get('rhea_id', '').strip()

    context = {
        'view_type': view_type,
        'rhea_id': rhea_id,
    }

    return render(request, 'rhea_widget/index.html', context)
