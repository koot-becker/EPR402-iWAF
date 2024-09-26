import numpy as np
from scipy.sparse import csr_matrix
import csv
from sklearn.feature_extraction.text import CountVectorizer as SimpleCountVectorizer

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

# Example usage:
if __name__ == "__main__":
    data_path = '/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
    labels = [row['Class'] for row in data]

    # Vectorize the text data
    vectorizer = SimpleCountVectorizer()
    sparse_data = vectorizer.fit_transform(texts)

    # Train the classifier
    classifier = ZScoreOutlierClassifier(threshold=2.0)
    classifier.fit(sparse_data)

    # Load the dataset from csic_final.csv
    data_path = '/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
    labels = [row['Class'] for row in data]

    X = vectorizer.transform(texts)

    outliers = classifier.predict(X)

    print(outliers)
