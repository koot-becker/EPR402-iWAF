import classifier
import csv

def classify_requests():
    # Load the dataset from csic_final.csv
    data_path = '/home/administrator/EPR402/WebAppFirewall/Classifier/Datasets/test.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] for row in data]
    labels = [row['Class'] for row in data]

    # Initialize counters for allowed and denied requests
    true_positive_count = 0
    false_positive_count = 0
    true_negative_count = 0
    false_negative_count = 0

    # Classify each request in the dataset
    for request in range(len(texts)):
        # Classify the request using method and URI
        classification = classifier.classify(texts[request])

        # Increment the respective counter based on the classification
        if classification == "Valid":
            if labels[request] == "Valid":
                true_positive_count += 1
            else:
                false_positive_count += 1
        elif classification == "Anomalous":
            if labels[request] == "Anomalous":
                true_negative_count += 1
            else:
                false_negative_count += 1

    # Calculate the percentage of requests allowed and denied
    total_positive_count = true_positive_count + false_negative_count
    total_negative_count = true_negative_count + false_positive_count
    total_count = total_positive_count + total_negative_count
    print(f'Total requests: {total_count}')
    allowed_percentage = (total_positive_count / total_count) * 100
    denied_percentage = (total_negative_count / total_count) * 100
    tpr = (true_positive_count / total_positive_count) * 100
    fpr = (false_positive_count / total_positive_count) * 100
    tnr = (true_negative_count / total_negative_count) * 100
    fnr = (false_negative_count / total_negative_count) * 100
    print(f'Total allowed percentage: {allowed_percentage}')
    print(f'Total denied percentage: {denied_percentage}')
    print(f'True positive percentage (TPR): {tpr}')
    print(f'False positive percentage: {fpr}')
    print(f'True negative percentage (TNR): {tnr}')
    print(f'False negative percentage: {fnr}')
    print(f'Balanced Accuracy: {(tpr + tnr) / 2}')

if __name__ == "__main__":
    classify_requests()
