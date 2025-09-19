from django.shortcuts import render

def index(request):
    summary_type = request.GET.get('summary_type', 'connected_only').strip()
    api_path = request.GET.get('api_path', '').strip()
    model_view_url = request.GET.get('model_view_url', '').strip()

    context = {
        'summary_type': summary_type,
        'api_path': api_path,
        'model_view_url': model_view_url
    }

    return render(request, 'gocam_connections/index.html', context)
