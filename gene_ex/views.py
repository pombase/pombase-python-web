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

        protein_plot_order = []
        rna_plot_order = []
        plot_conf = {}
        pubmed_ids = []

        for conf in website_config['gene_expression']['datasets']:
            key = (conf['pubmed_id'], conf['level_type'], conf['during'])
            if conf['level_type'] == 'protein level':
                protein_plot_order.append(conf['plot_display_name'])
            else:
                rna_plot_order.append(conf['plot_display_name'])
            plot_conf[key] = conf['plot_display_name']
            if not conf['pubmed_id'] in pubmed_ids:
                pubmed_ids.append(conf['pubmed_id'])

        return (protein_plot_order, rna_plot_order, plot_conf, pubmed_ids)

def read_gene_ex_df():
    protein_plot_order, rna_plot_order, plot_config, pubmed_ids = read_config()

    file_name = os.environ['GENE_EX_TSV_PATH']

    df = pd.read_csv(file_name, sep="\t", header=0)

    df = df[df.reference.isin(pubmed_ids)]
    df.loc[df['average_copies_per_cell'] < 0.0001, 'average_copies_per_cell'] = np.NaN

    df['dataset_name'] = df.apply(lambda x: plot_config[(x['reference'], x['term_name'], x['during_term_name'])],axis=1)

    df['log_average_copies_per_cell'] = np.log10(df['average_copies_per_cell']).fillna(0)

    protein_df = df[df['term_name'] == 'protein level']
    rna_df = df[df['term_name'] == 'RNA level']

    return (protein_plot_order, rna_plot_order, protein_df, rna_df)


protein_plot_order, rna_plot_order, protein_gene_ex_df, rna_gene_ex_df = None, None, None, None


def gene_ex_violin(request):
    global protein_plot_order, rna_plot_order, protein_gene_ex_df, rna_gene_ex_df

    if protein_plot_order == None:
        protein_plot_order, rna_plot_order, protein_gene_ex_df, rna_gene_ex_df = read_gene_ex_df()

    plot_order = [protein_plot_order, rna_plot_order]

    plot_size = request.GET.get('plot_size', '').strip()
    if plot_size == 'large':
        plt.rcParams['savefig.dpi'] = 175
    else:
        plt.rcParams['savefig.dpi'] = 100

    genes_param = request.GET.get('genes', '').strip()
    genes = genes_param.split(',')

    frames = [protein_gene_ex_df, rna_gene_ex_df]

    gene_frames = [frame[frame['gene'].isin(genes)] for frame in frames]

    gridspec = {
        'width_ratios': [frames[0]['dataset_name'].nunique(), frames[1]['dataset_name'].nunique()]
    }
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.5), gridspec_kw=gridspec)

#    fig.legend(fontsize='x-large', title_fontsize='30')

    sns.set(font_scale=0.5)

    axes[0].title.set_text('Protein expression')
    axes[1].title.set_text('RNA expression')

    gene_count = len(genes)

    swarm_dot_size = 10

    if gene_count > 0:
        if gene_count >= 5:
            swarm_dot_size = 7
        if gene_count >= 30:
            swarm_dot_size = 5
        if gene_count >= 60:
            swarm_dot_size = 3.5
        if gene_count >= 130:
            swarm_dot_size = 2.5

    for idx in [0,1]:
        ax = axes[idx]
        ax.title.set_fontsize(17)
        vp = sns.violinplot(ax=ax, order=plot_order[idx], scale="width", data=frames[idx], color="#bfcfef", x='dataset_name', y="log_average_copies_per_cell", inner="box")

        if gene_count > 0:
            sns.swarmplot(ax=ax, order=plot_order[idx], data=gene_frames[idx], size=swarm_dot_size, x='dataset_name', y="log_average_copies_per_cell", color="red")

#        ax.set_xlabel('Dataset', fontsize=12)
        ax.set_xlabel('', fontsize=12)
        ax.set_ylabel('log10(average number of molecules per cell)', fontsize=13)

        for col in ax.collections:
            col.set_edgecolor('#999')

        ax.tick_params(axis='y', which='both', labelsize=14);
        ax.set_xticklabels(plot_order[idx], fontsize=9);


    sns.despine()

    response = HttpResponse(content_type="image/png")
    fig.savefig(response, format="png")

    return response
