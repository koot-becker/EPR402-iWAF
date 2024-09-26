# Existing imports
import pickle

# Custom imports
from Vectorizer.count_vectorizer import SimpleCountVectorizer
from OutlierClassifier.outlier_classifier import ZScoreOutlierClassifier

def train_classifier(texts, labels):
    # Create the feature vectors
    vectorizer = SimpleCountVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train the classifier
    # classifier = MultinomialNaiveBayes()
    # classifier.fit(X, labels)
    
    classifier = ZScoreOutlierClassifier(threshold=2.0)
    classifier.fit(X)

    # Save the fitted CountVectorizer
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    # Save the trained classifiers
    with open('trained_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)

def classify(texts):
    # Load the trained classifiers
    with open('trained_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)

    # Load the fitted CountVectorizer
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    # Create the feature vector
    X = vectorizer.transform([texts])

    # Predict the class
    prediction = classifier.predict(X)

    return prediction[0]