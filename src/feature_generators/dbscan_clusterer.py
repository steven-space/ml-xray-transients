from sklearn.cluster import DBSCAN

def dbscan_clusterer(df_tsne, epsilon, min_samples):
    embedding = df_tsne[['tsne1', 'tsne2']].values
    dbscan_model = DBSCAN(eps=epsilon, min_samples=min_samples)
    clusters = dbscan_model.fit(embedding)
    labels = clusters.labels_
    return labels