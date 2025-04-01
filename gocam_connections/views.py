from django.shortcuts import render

def index(request):
    context = {
    }

    return render(request, 'gocam_connections/index.html', context)
