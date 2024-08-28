import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_classifier():
    # Load the legitimate dataset
    with open('legitimate_dataset.json', 'r') as f:
        legitimate_data = json.load(f)

    # Load the SQLi dataset
    with open('sqli_dataset.json', 'r') as f:
        sqli_data = json.load(f)

    # Combine the datasets
    data = legitimate_data + sqli_data

    # Create the feature vectors
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data)

    # Create the labels
    y = [0] * len(legitimate_data) + [1] * len(sqli_data)

    # Train the classifier
    classifier = MultinomialNB()
    classifier.fit(X, y)

    return classifier

def BaselineTrainer(classifier):
    while True:
        # Get user input
        user_input = input("Enter a text to classify (or 'q' to quit): ")

        # Check if user wants to quit
        if user_input == 'q':
            break

        # Vectorize the user input
        vectorizer = CountVectorizer()
        vectorized_input = vectorizer.transform([user_input])

        # Predict the class
        predicted_class = classifier.predict(vectorized_input)[0]

        # Print the predicted class
        if predicted_class == 0:
            return False
        else:
            return True

if __name__ == '__main__':
    # Train the classifier
    classifier = train_classifier()

    # Save the trained classifier
    with open('trained_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)