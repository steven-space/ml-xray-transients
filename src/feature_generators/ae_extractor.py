import tensorflow as tf
import numpy as np

def ae_extractor(histograms, encoder_path):
    tf.random.set_seed(42)
    encoder = tf.keras.models.load_model(encoder_path)
    histograms_array = np.array([np.array(h) for h in histograms])
    features_extracted_ae = encoder.predict(histograms_array)
    return features_extracted_ae