from sklearn.neighbors import NearestNeighbors
import pandas as pd

def knn_finder(df_bonafide, df_embedding, k):
    knn_model= NearestNeighbors(n_neighbors=k, metric='euclidean') 
    knn_model.fit(df_embedding[['tsne1', 'tsne2']])
    distances, indices = knn_model.kneighbors(df_bonafide[['tsne1', 'tsne2']])
    flat_indices = indices.flatten()
    df_knn = df_embedding.iloc[flat_indices].copy()
    return df_knn

