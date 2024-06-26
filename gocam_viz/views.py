from django.shortcuts import render

def index(request):
    full_or_widget = request.GET.get('full_or_widget', '').strip()
    gocam_id = request.GET.get('gocam_id', '').strip()

    if full_or_widget == 'widget':
        graph_height = 420
    else:
        graph_height = 650

    gocam_viz_html = f"<wc-gocam-viz style='--button-background: #2598c5; --button-background-hover: #2598c5; -- --button-color: #fff; --panel-header-border-width: 1px; --panel-header-border-color: #ddd; --border-color: #d1c4e9; --panel-header-padding: 0.2em; --panel-header-background: #f2f2f2; --graph-height: {graph_height}px;' id='gocam-1' api-url='https://api.geneontology.xyz/gocam/%ID/raw' gocam-id='{gocam_id}'></wc-gocam-viz>";

    context = {
#        'full_or_widget': full_or_widget,
#        'gene_uniquename': gene_uniquename
        'gocam_viz_html': gocam_viz_html,
    }

    return render(request, 'gocam_viz/index.html', context)
