from django.shortcuts import render

def index(request):
    summary_type = request.GET.get('summary_type', 'connected_only').strip()

    context = {
        'summary_type': summary_type,
    }

    return render(request, 'gocam_connections/index.html', context)
