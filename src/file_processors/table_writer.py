import pandas as pd

def embedding_writer(tsne_embedding, ids):
    df_tsne = pd.DataFrame(tsne_embedding, columns=['tsne1', 'tsne2'])
    df_tsne['obsreg_id'] = ids
    return df_tsne

def clustering_writer(df_tsne, labels):
    df_dbscan = df_tsne.copy()
    df_dbscan['cluster'] = labels
    df_dbscan = df_dbscan.sort_values(by='cluster', ascending=True) 
    return df_dbscan
