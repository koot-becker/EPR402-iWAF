import numpy as np

class MultinomialNaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.class_log_prior_ = None
        self.feature_log_prob_ = None
        self.classes_ = None

    def fit(self, X, y):
        # Identify unique classes
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]

        # Initialize counts
        class_count = np.zeros(n_classes)
        feature_count = np.zeros((n_classes, n_features))

        # Count occurrences
        for i, class_label in enumerate(self.classes_):
            X_class = X[y == class_label]
            class_count[i] = X_class.shape[0]
            feature_count[i, :] = X_class.sum(axis=0)

        # Compute log prior probabilities
        self.class_log_prior_ = np.log(class_count / class_count.sum())

        # Apply Laplace smoothing
        smoothed_fc = feature_count + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1) + self.alpha * n_features

        # Compute log probabilities
        self.feature_log_prob_ = np.log(smoothed_fc / smoothed_cc[:, np.newaxis])

    def predict(self, X):
        jll = self._joint_log_likelihood(X)
        return self.classes_[np.argmax(jll, axis=1)]

    def _joint_log_likelihood(self, X):
        return (X @ self.feature_log_prob_.T) + self.class_log_prior_

'''
Example usage:
X = np.array([[2, 1, 0], [1, 0, 1], [2, 0, 0], [0, 1, 2]])
y = np.array([0, 1, 0, 1])
model = MultinomialNaiveBayes()
model.fit(X, y)
predictions = model.predict(np.array([[1, 0, 1], [0, 2, 1]]))
print(predictions)
'''