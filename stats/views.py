from django.http import HttpResponse

import os
import json
import re

import io

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from matplotlib.ticker import MultipleLocator

sns.set_theme(style="whitegrid")

def read_config():
    with open(os.environ['WEBSITE_CONFIG_JSON_PATH'], "r") as json_file:
        website_config = json.load(json_file)

        return website_config

year_dec_re = re.compile('^(\d\d\d\d)-12')

def read_gene_ex_df(config):
    min_year = config['stats_page']['curated_vs_curatable_min_year']

    with open(os.environ['DETAILED_STATS_JSON'], "r") as json_file:
        stats = json.load(json_file)

        date = []
        curatable = []
        curated = []

        cumulative_data = stats['cumulative_pub_stats_by_month']['data']

        d = {'curatable': curatable, 'curated': curated }

        for row in cumulative_data:
            row_date = row[0]
            if row_date >= str(min_year):
                m = year_dec_re.match(row_date)
                if m:
                   curatable.append(row[1])
                   curated.append(row[2])
                   date.append(m.group(1))

        return pd.DataFrame(data=d, index=date)


config = read_config()

def cumulative_pub_stats_by_month(request):
    df = read_gene_ex_df(config)

    print(df)

    ax = sns.lineplot(data=df[['curated', 'curatable']], color="blue")

    ax.xaxis.set_major_locator(MultipleLocator(2))

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response
