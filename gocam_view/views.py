from django.shortcuts import render

def index(request):
    full_or_widget = request.GET.get('full_or_widget', '').strip()
    gocam_id = request.GET.get('gocam_id', '').strip()
    api_path = request.GET.get('api_path', '').strip()
    model_view_url = request.GET.get('model_view_url', '').strip()
    highlight_gene_ids = request.GET.get('highlight_gene_ids', '').strip()

    if full_or_widget == 'widget':
        graph_height = 420
    else:
        graph_height = 650

    context = {
        'full_or_widget': full_or_widget,
        'gocam_id': gocam_id,
        'api_path': api_path,
        'model_view_url': model_view_url,
        'highlight_gene_ids': highlight_gene_ids.split(','),
    }

    return render(request, 'gocam_view/index.html', context)
