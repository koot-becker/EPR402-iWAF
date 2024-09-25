# Existing imports
import numpy as np
from collections import defaultdict

def create_float_defaultdict():
    """
    Creates a defaultdict with float as the default factory.
    
    Returns:
        defaultdict: A defaultdict that returns 0.0 for missing keys.
    """
    return defaultdict(float)

def create_int_defaultdict():
    """
    Creates a defaultdict with int as the default factory.
    
    Returns:
        defaultdict: A defaultdict that returns 0 for missing keys.
    """
    return defaultdict(int)

class MultinomialNaiveBayes:
    """
    Implements the Multinomial Naive Bayes algorithm for classification.
    """

    def __init__(self, alpha=1.0):
        """
        Initializes the MultinomialNaiveBayes classifier.

        Args:
            alpha (float): Smoothing parameter for Laplace smoothing. Default is 1.0.
        """
        self.alpha = alpha  # Smoothing parameter
        self.class_priors = {}
        self.feature_probs = defaultdict(create_float_defaultdict)
        self.classes = set()
        self.vocabulary = set()

    def fit(self, X, y):
        """
        Fits the Multinomial Naive Bayes classifier to the training data.

        Args:
            X (scipy.sparse.csr_matrix): The input features as a sparse matrix.
            y (array-like): The target labels.
        """
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
        """
        Predicts the class labels for the input samples.

        Args:
            X (scipy.sparse.csr_matrix): The input features as a sparse matrix.

        Returns:
            list: Predicted class labels for each input sample.
        """
        return [self._predict_single(x) for x in X]

    def _predict_single(self, x):
        """
        Predicts the class label for a single input sample.

        Args:
            x (scipy.sparse.csr_matrix): A single input sample as a sparse matrix row.

        Returns:
            The predicted class label.
        """
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