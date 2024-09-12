import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

def create_float_defaultdict():
    return defaultdict(float)

def create_int_defaultdict():
    return defaultdict(int)

class MultinomialNaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Smoothing parameter
        self.class_priors = {}
        self.feature_probs = defaultdict(create_float_defaultdict)
        self.classes = set()
        self.vocabulary = set()

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.classes = set(y)
        
        # Calculate class priors
        class_counts = defaultdict(int)
        for label in y:
            class_counts[label] += 1
        
        for c in self.classes:
            self.class_priors[c] = class_counts[c] / n_samples

        # Calculate feature probabilities
        feature_counts = defaultdict(create_int_defaultdict)
        class_totals = defaultdict(int)

        for i in range(n_samples):
            c = y[i]
            for j in X[i].indices:
                feature_counts[c][j] += X[i, j]
                class_totals[c] += X[i, j]
                self.vocabulary.add(j)

        for c in self.classes:
            for feature in self.vocabulary:
                numerator = feature_counts[c][feature] + self.alpha
                denominator = class_totals[c] + self.alpha * len(self.vocabulary)
                self.feature_probs[c][feature] = numerator / denominator

    def predict(self, X):
        return [self._predict_single(x) for x in X]

    def _predict_single(self, x):
        best_class = None
        best_score = float('-inf')

        for c in self.classes:
            score = np.log(self.class_priors[c])
            for i in x.indices:
                score += x[0, i] * np.log(self.feature_probs[c][i])
            
            if score > best_score:
                best_score = score
                best_class = c

        return best_class

if __name__ == '__main__':
    training_data_path = '/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/csic_training.csv'
    with open(training_data_path, 'r') as file:
        reader = csv.DictReader(file)
        training_data = [row for row in reader]

    # Prepare the training data
    training_texts = [row['Method'] + ' ' + row['URI'] for row in training_data]
    training_labels = [row['Class'] for row in training_data]

    # Create the feature vectors
    vectorizer = CountVectorizer()
    training_X = vectorizer.fit_transform(training_texts)

    training_model = MultinomialNaiveBayes()
    training_model.fit(training_X, training_labels)

    # Load the dataset from csic_final.csv
    testing_data_path = '/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/training.csv'
    with open(testing_data_path, 'r') as file:
        reader = csv.DictReader(file)
        testing_data = [row for row in reader]

    # Prepare the training data
    testing_texts = [row['Method'] + ' ' + row['URI'] for row in testing_data]
    testing_labels = [row['Class'] for row in testing_data]

    for request in range(len(testing_texts)):
        # Create the feature vector
        testing_X = vectorizer.transform([testing_texts[request]])

        # Predict the class
        prediction = training_model.predict(testing_X)
        print(prediction)
