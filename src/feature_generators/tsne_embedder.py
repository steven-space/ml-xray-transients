from sklearn.manifold import TSNE


def tsne_embedder(features, perplexity, learning_rate, early_exaggeration, iterations, random_state, dimensions=2, init='random'):
    tsne_model = TSNE(n_components = dimensions, perplexity = perplexity, learning_rate = learning_rate, early_exaggeration = early_exaggeration, n_iter = iterations, init=init, random_state=random_state)
    features_embedded_tsne = tsne_model.fit_transform(features)
    return features_embedded_tsne
