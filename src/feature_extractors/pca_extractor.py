from sklearn.decomposition import PCA

def pca_extractor(histograms_flattened, num_components):
    pca_model = PCA(n_components=num_components)
    features_extracted_pca = pca_model.fit_transform(histograms_flattened)
    return features_extracted_pca



