from django.shortcuts import render

def index(request):
    summary_type = request.GET.get('summary_type', 'connected_only').strip()
    api_path = request.GET.get('api_path', '').strip()

    context = {
        'summary_type': summary_type,
        'api_path': api_path,
    }

    return render(request, 'gocam_connections/index.html', context)
