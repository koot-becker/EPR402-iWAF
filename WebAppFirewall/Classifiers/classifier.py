# Existing imports
import numpy as np
from collections import defaultdict
from scipy.spatial.distance import cdist
from scipy.sparse import csr_matrix

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

class OneClassSVMClassifier:
    """
    One-Class SVM Classifier for outlier detection using various kernels.

    Parameters
    ----------
    kernel : str, optional (default='rbf')
        Specifies the kernel type to be used in the algorithm. Supported options are 'rbf''.
        
    nu : float, optional (default=0.5)
        An upper bound on the fraction of margin errors and a lower bound of the fraction of support vectors. Should be in the interval (0, 1].

    gamma : {'scale', float}, optional (default='scale')
        Kernel coefficient for 'rbf' and 'poly'. If 'scale', it uses 1 / (n_features * X.var()) as value of gamma.

    degree : int, optional (default=3)
        Degree of the polynomial kernel function ('poly'). Ignored by other kernels.

    coef0 : float, optional (default=1)
        Independent term in polynomial kernel. It is only significant in 'poly' kernel.

    Attributes
    ----------
    alpha : ndarray of shape (n_samples,)
        Lagrange multipliers for the support vectors.

    support_vectors : ndarray of shape (n_samples, n_features)
        Support vectors.

    intercept : float
        Intercept term in the decision function.

    Methods
    -------
    fit(data)
        Fit the model using the training data.

    predict(data)
        Perform classification on samples in data.
    """
    def __init__(self, kernel='rbf', nu=0.5, gamma='scale', degree=3, coef0=1):
        self.kernel = kernel
        self.nu = nu
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.alpha = None
        self.support_vectors = None
        self.intercept = None

    def _rbf_kernel(self, X, Y):
        if self.gamma == 'scale':
            self.gamma = 1 / (X.shape[1] * X.var())
        return np.exp(-self.gamma * cdist(X, Y, 'sqeuclidean'))

    def _compute_kernel(self, X, Y):
        if self.kernel == 'rbf':
            return self._rbf_kernel(X, Y)
        else:
            raise ValueError(f"Unsupported kernel type: {self.kernel}")

    def fit(self, data):
        data = data.toarray() if isinstance(data, csr_matrix) else data
        n_samples = data.shape[0]

        # Compute the kernel matrix
        K = self._compute_kernel(data, data)

        # Solve the quadratic programming problem
        P = K
        q = -np.ones(n_samples)
        G = np.vstack((-np.eye(n_samples), np.eye(n_samples)))
        h = np.hstack((np.zeros(n_samples), np.ones(n_samples) / (n_samples * self.nu)))
        A = np.ones((1, n_samples))
        b = np.array([1.0])

        # Use a QP solver from scipy
        from scipy.optimize import linprog
        res = linprog(c=q, A_ub=G, b_ub=h, A_eq=A, b_eq=b, bounds=(0, None), method='highs')

        self.alpha = res.x
        self.support_vectors = data
        self.intercept = np.mean(K @ self.alpha)

    def predict(self, data):
        data = data.toarray() if isinstance(data, csr_matrix) else data
        K = self._compute_kernel(data, self.support_vectors)
        decision_function = K @ self.alpha - self.intercept
        return np.where(decision_function < 0, "Anomalous", "Valid")