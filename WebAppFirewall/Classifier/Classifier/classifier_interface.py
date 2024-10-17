# Existing imports
import pickle

# Custom imports
from Classifier.Classifier.count_vectorizer import SimpleCountVectorizer
from Classifier.Classifier.classifier import OneClassSVMClassifier, MultinomialNaiveBayes

def train_classifier(texts, labels, classifier_type='mnb'):
    # Create the feature vectors
    vectorizer = SimpleCountVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train the classifier
    if classifier_type == 'svm':
        classifier = OneClassSVMClassifier()
        classifier.fit(X)
    elif classifier_type == 'mnb':
        classifier = MultinomialNaiveBayes()
        classifier.fit(X, labels)
    else:
        raise ValueError("Invalid classifier type. Supported types: 'svm', 'mnb'.")

    # Save the fitted CountVectorizer
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/vectorizer_{classifier_type}.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    # Save the trained classifiers
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/classifier_{classifier_type}.pkl', 'wb') as f:
        pickle.dump(classifier, f)

def classify(texts, classifier_type='mnb'):
    # Load the trained classifiers
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/classifier_{classifier_type}.pkl', 'rb') as f:
        classifier = pickle.load(f)

    # Load the fitted CountVectorizer
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/vectorizer_{classifier_type}.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    # Create the feature vector
    X = vectorizer.transform([texts])

    # Predict the class
    prediction = classifier.predict(X)

    return prediction[0]