import pickle 
import numpy as np
import pandas as pd

def histogram_reader(histogram_file_path, properties_file_path, extractor_type):
    # Load histogram dictionary
    with open(histogram_file_path, 'rb') as f:
        hist_dict = pickle.load(f)
    # Flatten histograms in the dictionary and get IDs
    ids = list(hist_dict.keys())
    histograms = hist_dict.values()
    if extractor_type == 'PCA':
        histograms_array = np.array([np.array(h).flatten() for h in histograms])
    if extractor_type == 'AE':
        histograms_array = np.array([np.array(h) for h in histograms])
    # Load properties table and filter by IDs
    df_properties_input = pd.read_csv(properties_file_path)
    df_properties_input = df_properties_input[df_properties_input['obsreg_id'].isin(ids)]
    df_properties = df_properties_input.drop_duplicates('obsreg_id', keep='first').reset_index()
    return histograms_array, df_properties, ids