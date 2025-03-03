from django.shortcuts import render

def index(request):
    full_or_widget = request.GET.get('full_or_widget', '').strip()
    gocam_id = request.GET.get('gocam_id', '').strip()

    if full_or_widget == 'widget':
        graph_height = 420
    else:
        graph_height = 650

    context = {
        'full_or_widget': full_or_widget,
        'gocam_id': gocam_id,
    }

    return render(request, 'gocam_view/index.html', context)
