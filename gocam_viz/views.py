from django.shortcuts import render

def index(request):
    full_or_widget = request.GET.get('full_or_widget', '').strip()
    gene_uniquename = request.GET.get('gene_uniquename', '').strip()
    gocam_ids = request.GET.get('gocam_ids', '').strip().split(',')

    if len(gocam_ids) == 0:
        gocam_viz_html = f"No GO-CAM pathway for {gene_uniquename}";
    else:
        gocam_viz_html = f"<wc-gocam-viz id='gocam-1' api-url='https://api.geneontology.xyz/gocam/%ID/raw' gocam-id='{gocam_ids[0]}'></wc-gocam-viz>";

    context = {
#        'full_or_widget': full_or_widget,
#        'gene_uniquename': gene_uniquename
        'gocam_viz_html': gocam_viz_html,
    }

    return render(request, 'gocam_viz/index.html', context)
