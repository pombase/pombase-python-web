from django.shortcuts import render
from django.http import HttpResponse

import os
import json

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_theme(style="whitegrid")


def read_config():
    with open(os.environ['WEBSITE_CONFIG_JSON_PATH'], "r") as json_file:
        website_config = json.load(json_file)

        plot_order = []
        plot_conf = {}

        for conf in website_config['gene_expresion']['violin_plots']:
            key = (conf['pubmed_id'], conf['level_type'], conf['during'])
            plot_order.append(conf['display_name'])
            plot_conf[key] = conf['display_name']

        return (plot_order, plot_conf)

def read_gene_ex_df():
    plot_order, plot_config = read_config()

    file_name = os.environ['GENE_EX_TSV_PATH']

    df = pd.read_csv(file_name, sep="\t", header=0)
    df = df[~df['average_copies_per_cell'].str.startswith('>')]
    df['average_copies_per_cell'] = df['average_copies_per_cell'].astype('float64')
    df = df[(df['first_author'] == 'Marguerat') | (df['first_author'] == 'Carpy')]
    df.loc[df['average_copies_per_cell'] < 0.0001, 'average_copies_per_cell'] = np.NaN

    df['dataset_name'] = df.apply(lambda x: plot_config[(x['reference'], x['term_name'], x['during'])],axis=1)

    df['log_average_copies_per_cell'] = np.log10(df['average_copies_per_cell']).fillna(0)

    return (plot_order, df)


plot_order, gene_ex_df = None, None


def gene_ex_violin(request):
    global plot_order, gene_ex_df

    if plot_order == None:
       plot_order, gene_ex_df = read_gene_ex_df()

    genes_param = request.GET.get('genes', '').strip()
    genes = genes_param.split(',')
    genes_df = gene_ex_df[gene_ex_df['gene'].isin(genes)]

    fig, ax = plt.subplots(figsize=(20, 8))

    vp = sns.violinplot(ax=ax, order=plot_order, scale="width", data=gene_ex_df, palette="Set3", x='dataset_name', y="log_average_copies_per_cell", inner="box")

    if len(genes) > 0:
        sns.swarmplot(ax=ax, order=plot_order, data=genes_df, size=10, x='dataset_name', y="log_average_copies_per_cell", color="lightblue", edgecolor="black", linewidth=1)

    ax.set_xlabel('Gene expression dataset name', fontsize=14)
    ax.set_ylabel('log10(average number of molecules per cell)', fontsize=14)
    sns.despine()

    response = HttpResponse(content_type="image/png")
    fig.savefig(response, format="png")

    return response
