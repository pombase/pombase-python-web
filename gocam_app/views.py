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
            ids = form.cleaned_data["ids"].replace("\n", " ")
            ids = ids.replace("gomodel:", "");

            ids = re.sub(r'(?:\s|[,;])+', '+', ids)
            if not form.cleaned_data["dag"]:
                ids = 'B+' + ids
            ids = urllib.parse.quote_plus(ids)

            url = f"{app_path}/view/{ids}:show_models"

            return HttpResponseRedirect(url)

    else:
        form = IdForm()

    context["form"] = form

    return render(request, "gocam_app/index.html", context)
