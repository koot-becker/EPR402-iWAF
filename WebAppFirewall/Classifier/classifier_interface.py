# Existing imports
import pickle
# from sklearn.feature_extraction.text import CountVectorizer as SimpleCountVectorizer
# from sklearn.naive_bayes import MultinomialNB as MultinomialNaiveBayes

# Custom imports
from WebAppFirewall.Classifier.Vectorizer.count_vectorizer import SimpleCountVectorizer
from WebAppFirewall.Classifier.SignatureClassifier.signature_classifier import MultinomialNaiveBayes

def train_classifier(texts, labels):
    # Create the feature vectors
    vectorizer = SimpleCountVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train the classifier
    classifier = MultinomialNaiveBayes()
    classifier.fit(X, labels)

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