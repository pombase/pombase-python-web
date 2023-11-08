from django.http import HttpResponse

import os
import json
import re

import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from matplotlib.ticker import MultipleLocator


def read_config():
    with open(os.environ["WEBSITE_CONFIG_JSON_PATH"], "r") as json_file:
        website_config = json.load(json_file)

        return website_config


year_dec_re = re.compile("^(\d\d\d\d)-12")


def make_by_year_df(config, raw_stat_type, min_year):
    with open(os.environ["DETAILED_STATS_JSON"], "r") as json_file:
        stats = json.load(json_file)

        date = []
        curatable = []
        curated = []

        data = stats[raw_stat_type]["data"]

        d = {"curatable": curatable, "curated": curated}

        for row in data:
            row_date = row[0]
            if min_year is None or row_date >= str(min_year):
                date.append(row_date)
                curatable.append(row[1])
                curated.append(row[2])

        return pd.DataFrame(data=d, index=date)


def make_by_year_range_df(raw_stat_type):
    with open(os.environ["DETAILED_STATS_JSON"], "r") as json_file:
        stats = json.load(json_file)

        headers = stats[raw_stat_type]["header"][1::]

        data = stats[raw_stat_type]["data"]

        date_ranges = []
        frame_rows = []

        for row in data:
            date_range = row[0]
            date_ranges.append(date_range)
            frame_rows.append(row[1])

        return pd.DataFrame(data={headers[0]: frame_rows}, index=date_ranges)


config = read_config()


def make_plot(raw_stat_type, column_name=None):
    min_year = config["stats_page"]["curated_vs_curatable_min_year"]
    if column_name == "curatable":
        min_year = None

    df = make_by_year_df(config, raw_stat_type, min_year)

    plt.figure().clear()
    plt.rcParams["savefig.dpi"] = 15
    sns.set_theme(style="whitegrid")
    plt.tight_layout()

    if "cumulative" in raw_stat_type:
        ax = sns.lineplot(data=df)
    else:
        ax = sns.barplot(x=df.index, y=df[column_name], color="#8192ca")

    if column_name == "curatable":
        ax.xaxis.set_major_locator(MultipleLocator(10))
    else:
        ax.xaxis.set_major_locator(MultipleLocator(2))

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg", pad_inches=0.2, bbox_inches="tight")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response


def make_year_range_plot(raw_stat_type):
    df = make_by_year_range_df(raw_stat_type)

    plt.figure().clear()
    plt.rcParams["savefig.dpi"] = 15
    sns.set_theme(style="whitegrid")
    plt.tight_layout()
    plt.margins(x=0.5)

    ax = sns.barplot(x=df.index, y=df[df.columns[0]], color="#8192ca")

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.bar_label(ax.containers[0], fmt="%.1f")

    ax.set(ylabel=df.columns[0].replace("_", " "))

    #    ax.xaxis.set_major_locator(MultipleLocator(2))

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg", pad_inches=0.2, bbox_inches="tight")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response


def cumulative_curated_by_year(_):
    return make_plot('cumulative_curated_by_year')

def curated_by_year(_):
    return make_plot('curated_by_year', 'curated')

def curatable_by_year(_):
    return make_plot('curated_by_year', 'curatable')

def ltp_genes_per_pub_per_year_range(_):
    return make_year_range_plot('ltp_genes_per_pub_per_year_range')

def ltp_annotations_per_pub_per_year_range(_):
    return make_year_range_plot('ltp_annotations_per_pub_per_year_range')

def htp_annotations_per_pub_per_year_range(_):
    return make_year_range_plot('htp_annotations_per_pub_per_year_range')