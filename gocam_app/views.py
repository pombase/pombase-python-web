from django.http import HttpResponseRedirect
from django.shortcuts import render

import urllib.parse
import re

from .forms import IdForm

def index(request):
    app_path = request.GET.get('app_path', '').strip()
    api_path = request.GET.get('api_path', '').strip()

    context = {
        'app_path': app_path,
        'api_path': api_path,
    }

    if request.method == "POST":
        form = IdForm(request.POST)
        if form.is_valid():
            model_ids = form.cleaned_data["model_ids"].replace("\n", " ")
            model_ids = model_ids.replace("gomodel:", "");

            model_ids = re.sub(r'(?:\s|[,;])+', '+', model_ids)
            if not form.cleaned_data["dag"]:
                model_ids = 'B+' + model_ids
            model_ids = urllib.parse.quote_plus(model_ids)

            url = f"{app_path}/view/{model_ids}:show_models"

            if form.cleaned_data["targets"]:
                url += ',show_inputs'
            else:
                url += ',no_inputs'

            highlight_gene_ids = form.cleaned_data["highlight_gene_ids"].replace("\n", " ")

            if highlight_gene_ids != "":
                highlight_gene_ids = re.sub(r'(?:\s|[,;])+', ',', highlight_gene_ids)
                url += "/" + highlight_gene_ids

            print(url)

            return HttpResponseRedirect(url)

    else:
        form = IdForm()

    context["form"] = form

    return render(request, "gocam_app/index.html", context)
