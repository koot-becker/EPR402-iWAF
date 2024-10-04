package main

import (
	"encoding/gob"
	"fmt"
	"os"
)

// Define interfaces for the vectorizer and classifiers
type Vectorizer interface {
	FitTransform(texts []string) [][]float64
	Transform(texts []string) [][]float64
}

type Classifier interface {
	Fit(X [][]float64, labels []string)
	Predict(X [][]float64) []string
}

// Implement the trainClassifier function
func trainClassifier(texts, labels []string, classifierType string) error {
	var vectorizer Vectorizer
	var classifier Classifier

	// Create the feature vectors
	vectorizer = &SimpleCountVectorizer{}
	X := vectorizer.FitTransform(texts)

	// Train the classifier
	switch classifierType {
	case "svm":
		classifier = &OneClassSVMClassifier{}
		classifier.Fit(X, nil)
	case "mnb":
		classifier = &MultinomialNaiveBayes{}
		classifier.Fit(X, labels)
	default:
		return fmt.Errorf("invalid classifier type. Supported types: 'svm', 'mnb'")
	}

	// Save the fitted CountVectorizer
	vectorizerFile, err := os.Create(fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/vectorizer_%s.pkl", classifierType))
	if err != nil {
		return err
	}
	defer vectorizerFile.Close()
	encoder := gob.NewEncoder(vectorizerFile)
	if err := encoder.Encode(vectorizer); err != nil {
		return err
	}

	// Save the trained classifiers
	classifierFile, err := os.Create(fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/classifier_%s.pkl", classifierType))
	if err != nil {
		return err
	}
	defer classifierFile.Close()
	encoder = gob.NewEncoder(classifierFile)
	if err := encoder.Encode(classifier); err != nil {
		return err
	}

	return nil
}

// Implement the classify function
func classify(texts string, classifierType string) (string, error) {
	// Load the trained classifiers
	classifierFile, err := os.Open(fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/classifier_%s.pkl", classifierType))
	if err != nil {
		return "", err
	}
	defer classifierFile.Close()
	decoder := gob.NewDecoder(classifierFile)
	var classifier Classifier
	if err := decoder.Decode(&classifier); err != nil {
		return "", err
	}

	// Load the fitted CountVectorizer
	vectorizerFile, err := os.Open(fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Classifier/vectorizer_%s.pkl", classifierType))
	if err != nil {
		return "", err
	}
	defer vectorizerFile.Close()
	decoder = gob.NewDecoder(vectorizerFile)
	var vectorizer Vectorizer
	if err := decoder.Decode(&vectorizer); err != nil {
		return "", err
	}

	// Create the feature vector
	X := vectorizer.Transform([]string{texts})

	// Predict the class
	prediction := classifier.Predict(X)

	return prediction[0], nil
}
