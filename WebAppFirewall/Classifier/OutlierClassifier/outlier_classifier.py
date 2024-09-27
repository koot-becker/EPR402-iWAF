import numpy as np
from scipy.sparse import csr_matrix

class ZScoreOutlierClassifier:
    def __init__(self, threshold=3.0):
        self.threshold = threshold

    def fit(self, data):
        data = data.toarray() if isinstance(data, csr_matrix) else data
        self.mean = np.mean(data, axis=0)
        self.std = np.std(data, axis=0)

    def predict(self, data):
        data = data.toarray() if isinstance(data, csr_matrix) else data
        z_scores = (data - self.mean) / self.std
        outliers = np.any(np.abs(z_scores) > self.threshold, axis=1)
        return np.where(outliers, "Anomalous", "Valid")
