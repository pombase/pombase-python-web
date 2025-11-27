from django.shortcuts import render

def index(request):
    summary_type = request.GET.get('summary_type', 'connected_only').strip()
    api_path = request.GET.get('api_path', '').strip()
    flags = request.GET.get('flags', '').strip()
    model_view_path = request.GET.get('model_view_path', '').strip()

    context = {
        'summary_type': summary_type,
        'api_path': api_path,
        'flags': flags,
        'model_view_path': model_view_path
    }

    return render(request, 'gocam_connections/index.html', context)
