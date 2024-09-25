
import numpy as np
from scipy import stats
from typing import List, Tuple

class ZScoreOutlierClassifier:
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean = None
        self.std = None

    def fit(self, data: List[float]) -> None:
        """
        Fit the classifier with the input data.
        
        Args:
            data (List[float]): Input data to fit the classifier.
        """
        self.mean = np.mean(data)
        self.std = np.std(data)

    def predict(self, data: List[float]) -> List[bool]:
        """
        Predict outliers in the input data.
        
        Args:
            data (List[float]): Input data to classify.
        
        Returns:
            List[bool]: True for outliers, False for inliers.
        """
        if self.mean is None or self.std is None:
            raise ValueError("Classifier must be fitted before making predictions.")
        
        z_scores = np.abs(stats.zscore(data))
        return list(z_scores > self.threshold)

    def fit_predict(self, data: List[float]) -> List[bool]:
        """
        Fit the classifier and predict outliers in one step.
        
        Args:
            data (List[float]): Input data to fit and classify.
        
        Returns:
            List[bool]: True for outliers, False for inliers.
        """
        self.fit(data)
        return self.predict(data)

def detect_anomalies(requests: List[dict], feature: str, threshold: float = 3.0) -> Tuple[List[dict], List[dict]]:
    """
    Detect anomalies in web application firewall requests based on a specific feature.
    
    Args:
        requests (List[dict]): List of request dictionaries.
        feature (str): The feature to use for anomaly detection.
        threshold (float): Z-score threshold for outlier detection.
    
    Returns:
        Tuple[List[dict], List[dict]]: A tuple containing two lists: (normal_requests, anomalous_requests)
    """
    classifier = ZScoreOutlierClassifier(threshold)
    feature_values = [request.get(feature, 0) for request in requests]
    
    outliers = classifier.fit_predict(feature_values)
    
    normal_requests = [req for req, is_outlier in zip(requests, outliers) if not is_outlier]
    anomalous_requests = [req for req, is_outlier in zip(requests, outliers) if is_outlier]
    
    return normal_requests, anomalous_requests
