import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import json
import pandas as pd

def embedding_plotter(df, df_properties, color_code, bonafide_flares, bonafide_dips, bonafide_others):
    df = df.sort_values(by='obsreg_id', ascending=True)
    ids = df['obsreg_id'].values
    df_prop_reduced = df_properties[df_properties['obsreg_id'].isin(ids)]
    df_prop_reduced = df_prop_reduced.drop_duplicates('obsreg_id', keep='first')
    df_prop_reduced = df_prop_reduced.sort_values(by='obsreg_id', ascending=True)
    # Setup plot 
    if color_code == "clusters":
        fig, axs = plt.subplots(figsize=(6, 6),tight_layout = True)
        plt.subplots_adjust(bottom=0.5, right=1, top=1)
    elif bonafide_flares is not None and bonafide_dips is not None:
        fig, axs = plt.subplots(figsize=(8, 7))
    else:
        fig, axs = plt.subplots(figsize=(8, 6))
    axs.set_xlabel('t-SNE dimension 1')
    axs.set_ylabel('t-SNE dimension 2')

    # Settings depending on selected color property 
    if "hard" in color_code: 
        cmapcol = "Spectral"
        cbar_range = [-1,-0.5,0,0.5,1]
    elif "var_prob" in color_code:
        imperial = '#003E74'
        harvard = '#A51C30'
        silver = '#C0C0C0'
        cmapcol = mcolors.LinearSegmentedColormap.from_list('my_colormap', ['white',silver,'black'], N=256)
        cbar_range = [0, 0.2, 0.4, 0.6, 0.8, 1]
    elif "var_index" in color_code:
        gold = '#cfbd62'
        silver = '#C0C0C0'
        cmapcol = mcolors.LinearSegmentedColormap.from_list('my_colormap', ['white',silver,'black'], N=256)
        cbar_range = [0,1,2,3,4,5,6,7,8,9,10]
    elif color_code == "clusters":
        imperial = '#003E74'
        harvard = '#A51C30'
        silver = '#C0C0C0'
        gold = '#cfbd62'
        h_green = "#4db848"
        h_orange = "#f58549"
        h_purple = "#bb89ca"
        h_turq = "#00aaad"
        google_blue = '#4285F4'
        google_red = '#DB4437'
        google_yellow = '#F4B400'
        google_green = '#0F9D58'
        google_purple = '#7A6DAF'
        google_orange = '#E98119'
        google_turq = '#26929F'
        light_blue = '#98BCF9'
        light_red = '#EB9992'
        light_yellow = '#F9D674'
        light_green = '#7CCAA4'
        light_purple = '#B6AFD3'
        light_orange = '#F3BA82'
        light_turq = '#89C4CB'
        dark_blue = '#244985'
        dark_red = '#8B2B23'
        dark_yellow = '#B18300'
        dark_green = '#0A6438'
        dark_purple = '#4E456F'
        dark_orange = '#945210' 
        dark_turq = '#185D65'
        colors = [silver,'black',harvard,imperial,gold,h_green,h_purple,h_orange,google_turq,google_red,google_blue,google_yellow,google_green,google_purple,google_orange,h_turq, light_red, light_blue,light_yellow,light_green,  light_purple, light_orange, light_turq, dark_red,dark_blue, dark_yellow,  dark_green, dark_purple, dark_orange, dark_turq, 'red', 'blue', 'yellow', 'green', 'orange', 'magenta','cyan','brown','navy','gold','forestgreen']
        cmapcol = ListedColormap(colors[:len(df['cluster'].unique())])

    # Plot embeddings
    unique_labels = sorted(df['cluster'].unique())
    if color_code == "clusters":
        cluster = axs.scatter(df['tsne1'], df['tsne2'], s=0.1, c=df['cluster'], cmap=cmapcol)
        cluster_legend_handles = []
        for i in range(len(unique_labels)):
            if i > 0:
                label = 'Cluster ' + str(unique_labels[i])
                color = colors[i % len(colors)]
                cluster_legend_handles.append(mpatches.Patch(color=color, label=label))
            else:
                label = 'Outlier (0)'
                color = colors[i % len(colors)]
                cluster_legend_handles.append(mpatches.Patch(color=color, label=label))
        axs.set_title('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \n x \n x',c='white', loc='left')
        cluster_legend = axs.legend(handles=cluster_legend_handles, bbox_to_anchor=(1.02, 0.5), loc='center left', ncol=2, frameon=False, fontsize=8)
        axs.add_artist(cluster_legend)
    else:
        se = axs.scatter(df['tsne1'], df['tsne2'], c=df_prop_reduced[color_code], s=0.1, cmap=cmapcol)
        cbar_se = fig.colorbar(se, ax = axs)
        cbar_se.set_ticks(cbar_range)
        cbar_se.ax.set_ylabel(f'{color_code}', rotation = 0,labelpad=30)

    # Load bonafide flares and dips and others
    def load_json_data(file_path):
        if file_path is not None:
            with open(file_path, 'r') as file:
                return json.load(file)
        return None
    flare_groups = load_json_data(bonafide_flares)
    dip_groups = load_json_data(bonafide_dips)
    other_groups = load_json_data(bonafide_others)

    # Plot bonafide flares and dips and others
    def plot_group(groups, color, marker, label_suffix, axs):
        if groups is not None:
            df_group = []
            for index, (group, values) in enumerate(groups.items()):
                df_group_current = df[df['obsreg_id'].isin(values)]
                axs.scatter(df_group_current['tsne1'], df_group_current['tsne2'], edgecolors=color, marker=marker[index % len(marker)], facecolors='none', s=50, label=f"{group} {label_suffix}")
                df_group.append(df_group_current)
            df_group = pd.concat(df_group)
            return df_group, len(groups)
        else :
            return None, 0

    markers = ['s', 'o', '^', 'X', 'd', 'P', '*', 'v', '>', '<']
    df_dip_group, len_dip_group = plot_group(dip_groups, 'blue', markers, '(D)', axs)
    df_flare_group, len_flare_group = plot_group(flare_groups, 'red', markers, '(F)', axs)
    df_others_group, len_others_group = plot_group(other_groups, 'green', markers, '(O)', axs)
    total_groups = len_dip_group + len_flare_group + len_others_group
    dataframes = [df for df in [df_dip_group, df_flare_group, df_others_group] if df is not None]
    df_selected = pd.concat(dataframes) if dataframes else pd.DataFrame()

    if total_groups <= 12:
        axs.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3, frameon=False, fontsize=9.25)
    elif total_groups <= 16:
        axs.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, frameon=False, fontsize=9.25)
    else:
        print("Too many groups to plot legend with groups names")
        red_patch = mpatches.Patch(color='red', label='Flares')
        blue_patch = mpatches.Patch(color='blue', label='Dips')
        green_patch = mpatches.Patch(color='green', label='Others')
        axs.legend(handles=[red_patch, blue_patch, green_patch], loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3, frameon=False, fontsize=9.25)
    return unique_labels, df_dip_group, df_flare_group, df_others_group, df_selected


def embedding_plotter2(df_full, df_results, df_bonafide):
    imperial = '#003E74'
    harvard = '#A51C30'
    silver = '#C0C0C0'
    gold = '#cfbd62'
    h_orange = "#f58549"
    fig, axs = plt.subplots(figsize=(6.5, 6))
    axs.set_xlabel('t-SNE dimension 1')
    axs.set_ylabel('t-SNE dimension 2')
    axs.scatter(df_full['tsne1'], df_full['tsne2'], c=silver, s=1, label='Full Dataset')
    axs.scatter(df_results['tsne1'], df_results['tsne2'], c='black', s=2, label='Selected Subset')
    axs.scatter(df_bonafide['tsne1'], df_bonafide['tsne2'], c='magenta', s=10, marker = 'x', label='Bonafide Anomalies')
    axs.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False, fontsize=10)
    plt.show()

