import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB as MultinomialNaiveBayes
from classifier import MultinomialNaiveBayes

def train_classifier():
    # Load the training data
    data_path = '/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/csic_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
    labels = [row['Class'] for row in data]

    # Create the feature vectors
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train the classifier
    classifier = MultinomialNaiveBayes(alpha=0.5)
    classifier.fit(X, labels)

    return classifier, vectorizer

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

if __name__ == '__main__':
    # Train the classifier
    classifier, vectorizer = train_classifier()

    # Save the fitted CountVectorizer
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    # Save the trained classifiers
    with open('trained_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)