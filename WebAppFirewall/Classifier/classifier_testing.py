# Existing imports
import csv
import threading
import time

# Custom imports
import Classifier.classifier_interface as classifier_interface

def train_classifier(classifier_type='mnb', data='csic'):
    # Load the training data
    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/{data}_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
    labels = [row['Class'] for row in data]

    classifier_interface.train_classifier(texts, labels, classifier_type)

def classify_requests(classifier_type='mnb', data='csic'):
    # Load the dataset from csic_final.csv
    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/{data}_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
    labels = [row['Class'] for row in data]

    # Initialize counters for allowed and denied requests
    true_positive_count = 0
    false_positive_count = 0
    true_negative_count = 0
    false_negative_count = 0

    # Create a lock to synchronize access to the counters
    lock = threading.Lock()

    # Define a function to classify a single request
    def classify_request(request, classifier_type='mnb'):
        nonlocal true_positive_count, false_positive_count, true_negative_count, false_negative_count
        # Classify the request using method and URI
        classification = classifier_interface.classify(texts[request], classifier_type)

        # Increment the respective counter based on the classification
        if classification == "Valid":
            if labels[request] == "Valid":
                with lock:
                    true_positive_count += 1
            else:
                with lock:
                    false_positive_count += 1
        elif classification == "Anomalous":
            if labels[request] == "Anomalous":
                with lock:
                    true_negative_count += 1
            else:
                with lock:
                    false_negative_count += 1

    # Create a list to store the threads
    threads = []

    # Classify each request in the dataset using multiple threads
    count = 0
    for request in range(len(texts)):
        thread = threading.Thread(target=classify_request, args=(request,classifier_type))
        thread.start()
        threads.append(thread)
        count += 1
        if count % 10 == 0:
            print(f'{count} requests classified')

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Calculate the percentage of requests allowed and denied
    total_valid_count = true_positive_count + false_negative_count
    total_anomalous_count = true_negative_count + false_positive_count
    total_count = total_valid_count + total_anomalous_count
    print(f'Total requests: {total_count}')
    allowed_percentage = ((true_positive_count + false_positive_count) / total_count) * 100
    denied_percentage = ((true_negative_count + false_negative_count) / total_count) * 100
    tpr = (true_positive_count / total_valid_count) * 100
    fpr = (false_positive_count / total_anomalous_count) * 100
    tnr = (true_negative_count / total_anomalous_count) * 100
    fnr = (false_negative_count / total_valid_count) * 100
    print(f'Total allowed percentage: {allowed_percentage}')
    print(f'Total denied percentage: {denied_percentage}')
    print(f'True positive percentage (TPR): {tpr}')
    print(f'False positive percentage: {fpr}')
    print(f'True negative percentage (TNR): {tnr}')
    print(f'False negative percentage: {fnr}')
    print(f'Balanced Accuracy: {(tpr + tnr) / 2}')

if __name__ == "__main__":
    # classifier_type = 'mnb'
    classifier_type = 'svm'
    # data = 'csic'
    # data = 'combined'
    # data = 'ecml'
    data = 'outlier'
    start_time = time.perf_counter()
    train_classifier(classifier_type, data)
    classify_requests(classifier_type, data)
    end_time = time.perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')
