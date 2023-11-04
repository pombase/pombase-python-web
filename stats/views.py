from django.http import HttpResponse

import os
import json

import io

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_theme(style="whitegrid")

def read_config():
    with open(os.environ['WEBSITE_CONFIG_JSON_PATH'], "r") as json_file:
        website_config = json.load(json_file)

        return website_config

def read_gene_ex_df(config):
    min_year = config['stats_page']['curated_vs_curatable_min_year']

    with open(os.environ['DETAILED_STATS_JSON'], "r") as json_file:
        stats = json.load(json_file)

        date = []
        curatable = []
        curated = []

        cumulative_data = stats['cumulative_pub_stats_by_month']['data']

        d = {'date': date, 'curatable': curatable, 'curated': curated }

        for row in cumulative_data:
            if row[0] >= str(min_year):
                date.append(row[0])
                curatable.append(row[1])
                curated.append(row[2])

        return pd.DataFrame(data=d)


config = read_config()

def cumulative_pub_stats_by_month(request):
    df = read_gene_ex_df(config)

    sns.lineplot(data=df[['curated', 'curatable']], color="blue")

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response
