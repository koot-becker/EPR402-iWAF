# Existing imports
import pickle
import sys

# Custom imports
sys.path.append("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifiers/")
from count_vectorizer import SimpleCountVectorizer
from classifier import OneClassSVMClassifier, MultinomialNaiveBayes

def train_classifier(texts, labels, classifier_type='mnb', dataset='csic', alpha=1.0):
    # Create the feature vectors
    vectorizer = SimpleCountVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train the classifier
    if classifier_type == 'svm':
        classifier = OneClassSVMClassifier(nu=alpha)
        classifier.fit(X)
    elif classifier_type == 'mnb':
        classifier = MultinomialNaiveBayes(alpha=alpha)
        classifier.fit(X, labels)
    else:
        raise ValueError("Invalid classifier type. Supported types: 'svm', 'mnb'.")

    # Save the fitted CountVectorizer
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifiers/vectorizer_{classifier_type}_{dataset}.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    # Save the trained classifiers
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifiers/classifier_{classifier_type}_{dataset}.pkl', 'wb') as f:
        pickle.dump(classifier, f)

def classify(texts, classifier_type='mnb', dataset='csic'):
    # Load the trained classifiers
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifiers/classifier_{classifier_type}_{dataset}.pkl', 'rb') as f:
        classifier = pickle.load(f)

    # Load the fitted CountVectorizer
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifiers/vectorizer_{classifier_type}_{dataset}.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    # Create the feature vector
    X = vectorizer.transform([texts])

    # Predict the class
    prediction = classifier.predict(X)

    return prediction[0]