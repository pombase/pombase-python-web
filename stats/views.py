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

def read_detailed_stats():
    with open(os.environ["DETAILED_STATS_JSON"], "r") as json_file:
        stats = json.load(json_file)

        return stats


config = read_config()

detailed_stats = read_detailed_stats()


year_dec_re = re.compile("^(\d\d\d\d)-12")


def make_by_year_df(config, raw_stat_type, min_year):
        date = []
        curatable = []
        curated = []

        data = detailed_stats[raw_stat_type]["data"]

        d = {"curatable": curatable, "curated": curated}

        for row in data:
            row_date = row[0]
            if min_year is None or row_date >= str(min_year):
                date.append(row_date)
                curatable.append(row[1][0])
                curated.append(row[1][1])

        return pd.DataFrame(data=d, index=date)


def make_by_year_range_df(raw_stat_type):
        headers = detailed_stats[raw_stat_type]["header"][1::]

        data = detailed_stats[raw_stat_type]["data"]

        date_ranges = []
        frame_rows = []

        for row in data:
            date_range = row[0]
            date_ranges.append(date_range)
            frame_rows.append(row[1])

        return pd.DataFrame(data={headers[0]: frame_rows}, index=date_ranges)



def make_plot(raw_stat_type, column_name=None):
    min_year = config["stats"]["curated_vs_curatable_min_year"]
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

    fontsize = 14

    if 'htp' in raw_stat_type:
        fontsize = 12

    ax.bar_label(ax.containers[0], fmt="%.1f", fontsize=fontsize)

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

def community_response_rates(_):
    data = detailed_stats['community_response_rates']

    years = []
    response_rates = []

    x_min = 9999
    x_max = 0

    y_max = 0

    for row in data:
        years.append(row['year'])
        response_rates.append(row['response_rate'])
        if row['year'] < x_min:
            x_min = row['year']
        if row['year'] > x_max:
            x_max = row['year']
        if row['response_rate']:
            y_max = row['response_rate']

    df = pd.DataFrame(index=years, data={'response_rate': response_rates})

    plt.figure().clear()
    plt.rcParams["savefig.dpi"] = 15
    sns.set_theme(style="whitegrid")
    plt.tight_layout()
    plt.margins(x=0.5)
    y_max = y_max+5
    plt.ylim(0,y_max)
    plt.xlim(x_min, x_max)

    ax = sns.lineplot(data=df)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    ax.set(ylabel=df.columns[0].replace("_", " "))

    #    ax.xaxis.set_major_locator(MultipleLocator(2))

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg", pad_inches=0.2, bbox_inches="tight")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response


def raw_cumulative_annotation_type_counts_by_year():
    raw_stats = detailed_stats['cumulative_annotation_type_counts_by_year']

    years = []
    df_data = {}

    for (idx, header_name) in enumerate(raw_stats['header']):
        df_data[header_name] = []

    for row in raw_stats['data']:
        row_year = row[0]
        years.append(row_year)
        row_data = row[1]

        for (idx, header_name) in enumerate(raw_stats['header']):
            df_data[header_name].append(row_data[idx])

    raw_df = pd.DataFrame(index=years, data=df_data)

    return raw_df

def cumulative_annotation_type_counts_by_year(_):
    raw_df = raw_cumulative_annotation_type_counts_by_year()

    stats_config = config['stats']
    min_year = stats_config['annotation_type_counts_min_year']
    group_config = stats_config['annotation_type_groups']

    raw_index = raw_df.index

    df = pd.DataFrame(index=raw_index, data={})

    for group_conf in group_config:
        cv_names = group_conf['cv_names']
        for cv_name in cv_names:
            if cv_name not in raw_df.columns:
                raw_df[cv_name] = 0
        df[group_conf['display_name']] = raw_df[cv_names].sum(axis=1)


    df = df[df.index >= str(min_year-1)]
    df.rename(index={f"{min_year-1}": f"<{min_year}"}, inplace=True)

    plt.figure().clear()

    plt.rcParams["savefig.dpi"] = 15

    sns.set_palette('pastel')
    sns.set(rc={"figure.figsize":(8, 4)})
    sns.set_theme(style="whitegrid")

    plt.tight_layout()
    plt.margins(x=0.5)

    ax = df.plot(kind='bar', stacked=True)

    for container in ax.containers:
        plt.setp(container, width=0.8)


    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    #    ax.set(ylabel=df.columns[0].replace("_", " "))

    #    ax.xaxis.set_major_locator(MultipleLocator(2))

    imgdata = io.BytesIO()
    plt.savefig(imgdata, format="svg", pad_inches=0.2, bbox_inches="tight")

    response = HttpResponse(imgdata.getvalue(), content_type="image/svg+xml")

    return response
