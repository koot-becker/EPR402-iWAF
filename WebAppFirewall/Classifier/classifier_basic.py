import math

class GaussianNaiveBayes:
    def __init__(self):
        self.classes = {}
        self.class_probabilities = {}

    def fit(self, X, y):
        # Calculate class probabilities
        total_samples = len(y)
        unique_classes = set(y)
        for class_label in unique_classes:
            class_samples = X[y == class_label]
            self.classes[class_label] = class_samples
            self.class_probabilities[class_label] = len(class_samples) / total_samples

    def predict(self, X):
        predictions = []
        for sample in X:
            max_probability = -math.inf
            predicted_class = None
            for class_label in self.classes:
                class_samples = self.classes[class_label]
                class_probability = self.class_probabilities[class_label]
                likelihood = 1
                for i in range(len(sample)):
                    feature = sample[i]
                    mean = class_samples[:, i].mean()
                    std = class_samples[:, i].std()
                    likelihood *= self.calculate_gaussian_probability(feature, mean, std)
                posterior_probability = class_probability * likelihood
                if posterior_probability > max_probability:
                    max_probability = posterior_probability
                    predicted_class = class_label
            predictions.append(predicted_class)
        return predictions

    def calculate_gaussian_probability(self, x, mean, std):
        exponent = math.exp(-((x - mean) ** 2) / (2 * std ** 2))
        return (1 / (math.sqrt(2 * math.pi) * std)) * exponent