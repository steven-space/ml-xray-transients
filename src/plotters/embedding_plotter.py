import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json

def embedding_plotter(df, df_properties, color_property, bonafide_flares, bonafide_dips):
    # Setup plot 
    if bonafide_flares is not None and bonafide_dips is not None:
        fig, axs = plt.subplots(figsize=(8, 7))
    else:
        fig, axs = plt.subplots(figsize=(8, 6))
    axs.set_xlabel('t-SNE dimension 1')
    axs.set_ylabel('t-SNE dimension 2')

    # Settings depending on selected color property 
    if "hard" in color_property:
        cmapcol = "Spectral"
        cbar_range = [-1,-0.5,0,0.5,1]
    elif "var_prob" in color_property:
        imperial = '#003E74'
        harvard = '#A51C30'
        cmapcol = mcolors.LinearSegmentedColormap.from_list('my_colormap', [imperial,'white',harvard], N=256)
        cbar_range = [0, 0.2, 0.4, 0.6, 0.8, 1]
    elif "var_index" in color_property:
        gold = '#cfbd62'
        cmapcol = mcolors.LinearSegmentedColormap.from_list('my_colormap', ['white',gold,'black'], N=256)
        cbar_range = [0,1,2,3,4,5,6,7,8,9,10]

    # Plot embeddings
    se = axs.scatter(df['tsne1'], df['tsne2'], c=df_properties[color_property], s=0.1, cmap=cmapcol)
    cbar_se = fig.colorbar(se, ax = axs)
    cbar_se.set_ticks(cbar_range)
    cbar_se.ax.set_ylabel(f'{color_property}', rotation = 0,labelpad=30)
    if bonafide_flares is not None and bonafide_dips is not None:
        with open(bonafide_flares, 'r') as file:
            flare_groups = json.load(file)
        with open(bonafide_dips, 'r') as file:
            dip_groups = json.load(file)
    elif bonafide_flares is not None and bonafide_dips is None:
        with open(bonafide_flares, 'r') as file:
            flare_groups = json.load(file)
            dip_groups = None
    elif bonafide_flares is None and bonafide_dips is not None:
        with open(bonafide_dips, 'r') as file:
            dip_groups = json.load(file)
            flare_groups = None
    else:   
        flare_groups = None
        dip_groups = None

    # Plot bonafide flares and dips
    markers = ['s', 'o', '^', 'X', 'd', 'P', '*']
    if dip_groups is not None:
        for index, (dip_group, values) in enumerate(dip_groups.items()):
            df_dip_group = df[df['obsreg_id'].isin(values)]
            axs.scatter(df_dip_group['tsne1'], df_dip_group['tsne2'], edgecolors='blue', marker = markers[index], facecolors='none', s = 50, label = dip_group)
            axs.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3, frameon = False,fontsize=9.25)
    if flare_groups is not None:
        for index, (flare_group, values) in enumerate(flare_groups.items()):
            df_flare_group = df[df['obsreg_id'].isin(values)]
            axs.scatter(df_flare_group['tsne1'], df_flare_group['tsne2'], edgecolors='red', marker = markers[index], facecolors='none', s = 50, label = flare_group)
            axs.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3, frameon = False,fontsize=9.25)
    return None

    


