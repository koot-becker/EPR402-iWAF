package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"sync"
	"time"
)

func trainClassifier(classifierType, data string) {
	// Load the training data
	dataPath := fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/%s_training.csv", data)
	file, err := os.Open(dataPath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	// Prepare the training data
	var texts, labels []string
	for _, row := range records[1:] {
		texts = append(texts, row[0]+" "+row[1]+" "+row[2]+" "+row[3])
		labels = append(labels, row[4])
	}

	classifier_interface.TrainClassifier(texts, labels, classifierType)
}

func classifyRequests(classifierType, data string) {
	// Load the dataset from csic_final.csv
	dataPath := fmt.Sprintf("/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/%s_testing.csv", data)
	file, err := os.Open(dataPath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	// Prepare the training data
	var texts, labels []string
	for _, row := range records[1:] {
		texts = append(texts, row[0]+" "+row[1]+" "+row[2]+" "+row[3])
		labels = append(labels, row[4])
	}

	// Initialize counters for allowed and denied requests
	var truePositiveCount, falsePositiveCount, trueNegativeCount, falseNegativeCount int
	var lock sync.Mutex

	// Define a function to classify a single request
	classifyRequest := func(request int) {
		classification := classifier_interface.Classify(texts[request], classifierType)

		lock.Lock()
		defer lock.Unlock()
		if classification == "Valid" {
			if labels[request] == "Valid" {
				truePositiveCount++
			} else {
				falsePositiveCount++
			}
		} else if classification == "Anomalous" {
			if labels[request] == "Anomalous" {
				trueNegativeCount++
			} else {
				falseNegativeCount++
			}
		}
	}

	// Create a list to store the threads
	var wg sync.WaitGroup

	// Classify each request in the dataset using multiple threads
	for request := range texts {
		wg.Add(1)
		go func(req int) {
			defer wg.Done()
			classifyRequest(req)
		}(request)
	}

	// Wait for all threads to complete
	wg.Wait()

	// Calculate the percentage of requests allowed and denied
	totalValidCount := truePositiveCount + falseNegativeCount
	totalAnomalousCount := trueNegativeCount + falsePositiveCount
	totalCount := totalValidCount + totalAnomalousCount

	allowedPercentage := (float64(truePositiveCount+falsePositiveCount) / float64(totalCount)) * 100
	deniedPercentage := (float64(trueNegativeCount+falseNegativeCount) / float64(totalCount)) * 100
	tpr := (float64(truePositiveCount) / float64(totalValidCount)) * 100
	fpr := (float64(falsePositiveCount) / float64(totalAnomalousCount)) * 100
	tnr := (float64(trueNegativeCount) / float64(totalAnomalousCount)) * 100
	fnr := (float64(falseNegativeCount) / float64(totalValidCount)) * 100

	fmt.Printf("Total requests: %d\n", totalCount)
	fmt.Printf("Total allowed percentage: %.2f\n", allowedPercentage)
	fmt.Printf("Total denied percentage: %.2f\n", deniedPercentage)
	fmt.Printf("True positive percentage (TPR): %.2f\n", tpr)
	fmt.Printf("False positive percentage: %.2f\n", fpr)
	fmt.Printf("True negative percentage (TNR): %.2f\n", tnr)
	fmt.Printf("False negative percentage: %.2f\n", fnr)
	fmt.Printf("Balanced Accuracy: %.2f\n", (tpr+tnr)/2)

	// plot(tpr, tnr, classifierType)
}

func main() {
	classifierType := "svm"
	data := "outlier"
	startTime := time.Now()
	trainClassifier(classifierType, data)
	classifyRequests(classifierType, data)
	endTime := time.Now()
	fmt.Printf("Time taken: %v seconds\n", endTime.Sub(startTime).Seconds())
}
