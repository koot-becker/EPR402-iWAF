# Existing imports
import csv
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Custom imports
import Classifiers.classifier_interface as classifier_interface

def split_dataset(dataset, training_ratio=10):
    # Load the data
    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/Original/{dataset}.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Split the data
    valid_data = [row for row in data if row['Class'] == 'Valid']
    anomalous_data = [row for row in data if row['Class'] == 'Anomalous']

    # Shuffle the data
    np.random.shuffle(valid_data)
    np.random.shuffle(anomalous_data)

    # Shuffled data
    valid_data = valid_data[:int(len(valid_data) * 0.05)]
    anomalous_data = anomalous_data[:int(len(anomalous_data) * 0.05)]

    # Create the split point
    valid_split_point = int(len(valid_data) * (training_ratio / 100))
    anomalous_split_point = int(len(anomalous_data) * (training_ratio / 100))


    # Split the data
    training_data = valid_data[:valid_split_point] + anomalous_data[:anomalous_split_point]
    testing_data = valid_data[valid_split_point:] + anomalous_data[anomalous_split_point:]

    return training_data, testing_data

def train_classifier(classifier_type='mnb', dataset='csic', data=[]):
    if classifier_type == 'mnb':
        # Prepare the training data
        texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
        labels = [row['Class'] for row in data]
    elif classifier_type == 'svm':
        if dataset == 'tiredful':
            texts = [row['URI'] + ' ' + row['User-Role'] + ' ' + row['Method'] for row in data]
        elif dataset == 'dvwa':
            texts = [row['URI'] for row in data]
        elif dataset == 'ctf':
            texts = [row['URI'] + ' ' + row['Method'] for row in data]
        labels = [row['Class'] for row in data]
    else:
        raise ValueError("Invalid classifier type")

    classifier_interface.train_classifier(texts, labels, classifier_type, dataset)
    return

def classify_requests(classifier_type='mnb', dataset='csic', data=[]):
    # Prepare the training data
    if classifier_type == 'mnb':
        texts = [row['Method'] + ' ' + row['URI'] + ' ' + row['POST-Data'] + ' ' + row['GET-Query'] for row in data]
        labels = [row['Class'] for row in data]
    elif classifier_type == 'svm':
        if dataset == 'tiredful':
            texts = [row['URI'] + ' ' + row['User-Role'] + ' ' + row['Method'] for row in data]
        elif dataset == 'dvwa':
            texts = [row['URI'] for row in data]
        elif dataset == 'ctf':
            texts = [row['URI'] + ' ' + row['Method'] for row in data]
        labels = [row['Class'] for row in data]
    else:
        raise ValueError("Invalid classifier type")

    # Initialize counters for allowed and denied requests
    true_positive_count = 0
    false_positive_count = 0
    true_negative_count = 0
    false_negative_count = 0

    # Create a lock to synchronize access to the counters
    lock = threading.Lock()

    # Define a function to classify a single request
    def classify_request(request, classifier_type='mnb', dataset='csic'):
        nonlocal true_positive_count, false_positive_count, true_negative_count, false_negative_count
        # Classify the request using method and URI
        classification = classifier_interface.classify(texts[request], classifier_type, dataset)

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
        thread = threading.Thread(target=classify_request, args=(request, classifier_type, dataset))
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
    # total_count = total_valid_count + total_anomalous_count
    tpr = (true_positive_count / total_valid_count) * 100
    # fpr = (false_positive_count / total_anomalous_count) * 100
    tnr = (true_negative_count / total_anomalous_count) * 100
    # fnr = (false_negative_count / total_valid_count) * 100
    balanced_accuracy = (tpr + tnr) / 2

    return balanced_accuracy, tpr, tnr

def test_signature_classifier(split=10):  
    # CSIC
    csic_data = split_dataset(dataset='csic', training_ratio=split)
    train_classifier(classifier_type='mnb', dataset='csic', data=csic_data[0])
    csic_balanced, csic_tpr, csic_tnr = classify_requests(classifier_type='mnb', dataset='csic', data=csic_data[1])

    # ECML
    ecml_data = split_dataset(dataset='ecml', training_ratio=split)
    train_classifier(classifier_type='mnb', dataset='ecml', data=ecml_data[0])
    ecml_balanced, ecml_tpr, ecml_tnr = classify_requests(classifier_type='mnb', dataset='ecml', data=ecml_data[1])

    # Combined
    combined_data = split_dataset(dataset='combined', training_ratio=split)
    train_classifier(classifier_type='mnb', dataset='combined', data=combined_data[0])
    combined_balanced, combined_tpr, combined_tnr = classify_requests(classifier_type='mnb', dataset='combined', data=combined_data[1])

    return csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr

def test_anomaly_classifier(dataset_name='ctf'):
    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/GoBuster/{dataset_name}_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        training_data = [row for row in reader]

    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/GoBuster/{dataset_name}_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        testing_data = [row for row in reader]

    train_classifier(classifier_type='svm', dataset=dataset_name, data=training_data)

    return classify_requests(classifier_type='svm', dataset=dataset_name, data=testing_data)

def get_signature_results():
    csic_tpr = []
    ecml_tpr = []
    combined_tpr = []
    csic_tnr = []
    ecml_tnr = []
    combined_tnr = []
    for i in range(5, 10, 5):
        print(f'Split {i}:')
        results = test_signature_classifier(split=i)
        csic_tpr.append(results[0])
        ecml_tpr.append(results[1])
        combined_tpr.append(results[2])
        csic_tnr.append(results[3])
        ecml_tnr.append(results[4])
        combined_tnr.append(results[5])

    with open('balanced_accuracies.pkl', 'wb') as f:
        pickle.dump({'csic_tpr': csic_tpr, 'ecml_tpr': ecml_tpr, 'combined_tpr': combined_tpr, 'csic_tnr': csic_tnr, 'ecml_tnr': ecml_tnr, 'combined_tnr': combined_tnr}, f)

    return csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr

def get_anomaly_results():
    tpr = []
    tnr = []
    balanced = []

    results = test_anomaly_classifier(dataset_name='ctf')
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])

    results = test_anomaly_classifier(dataset_name='dvwa')
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])

    results = test_anomaly_classifier(dataset_name='tiredful')
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])        
    
    with open('svm_accuracies.pkl', 'wb') as f:
        pickle.dump({'balanced': balanced, 'tpr': tpr, 'tnr': tnr}, f)

    return balanced, tpr, tnr

def plot_balanced(csic_balanced, ecml_balanced, combined_balanced):
    x = np.arange(5, 55, 5)
    width = 1
    y_ticks = np.arange(0, 110, 10)
    x_ticks = np.arange(0, 55, 5)

    colors = ['red', 'tan', 'lime']
    labels = ['CSIC', 'ECML', 'Combined']

    plt.bar(x - width, csic_balanced, width=width, color=colors[0], label=labels[0])
    plt.bar(x, ecml_balanced, width=width, color=colors[1], label=labels[1])
    plt.bar(x + width, combined_balanced, width=width, color=colors[2], label=labels[2])
    plt.legend(prop={'size': 10}, loc='upper right')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Training Split (%)')
    plt.ylim([0, 100])
    plt.xlim([0, 55])
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    plt.title('Classifier Balanced Accuracy')

    plt.tight_layout()
    plt.show()

def plot_tpr_tnr(csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr):
    x = np.arange(5, 55, 5)
    width = 1
    y_ticks = np.arange(0, 110, 10)
    x_ticks = np.arange(0, 55, 5)

    colors = ['red', 'tan', 'lime']
    labels = ['CSIC', 'ECML', 'Combined']

    fig, (ax1,  ax2) = plt.subplots(2, 1)

    ax1.bar(x - width, csic_tpr, width=width, color=colors[0], label=labels[0])
    ax1.bar(x, ecml_tpr, width=width, color=colors[1], label=labels[1])
    ax1.bar(x + width, combined_tpr, width=width, color=colors[2], label=labels[2])
    ax1.legend(prop={'size': 10}, loc='upper right')
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_xlabel('Training Split (%)')
    ax1.set_ylim([0, 100])
    ax1.set_xlim([0, 55])
    ax1.set_yticks(y_ticks)
    ax1.set_xticks(x_ticks)
    ax1.set_title('Classifier True Positive Rate')

    ax2.bar(x - width, csic_tnr, width=width, color=colors[0], label=labels[0])
    ax2.bar(x, ecml_tnr, width=width, color=colors[1], label=labels[1])
    ax2.bar(x + width, combined_tnr, width=width, color=colors[2], label=labels[2])
    ax2.legend(prop={'size': 10}, loc='upper right')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_xlabel('Training Split (%)')
    ax2.set_ylim([0, 100])
    ax2.set_xlim([0, 55])
    ax2.set_yticks(y_ticks)
    ax2.set_xticks(x_ticks)
    ax2.set_title('Classifier True Negative Rate')

    plt.tight_layout()
    plt.show()

def plot_anomaly(balanced, tpr, tnr):
    x = np.arange(1, 4, 1)
    width = 0.2
    y_ticks = np.arange(0, 110, 10)
    x_ticks = ['CTF-JWT', 'DVWA', 'TIREDFUL']

    colors = ['red', 'tan', 'lime']
    labels = ['Balanced', 'TPR', 'TNR']

    plt.bar(x - 0.2, tnr, width=width, color=colors[0], label=labels[2])
    plt.bar(x, tpr, width=width, color=colors[2], label=labels[1])
    plt.bar(x + 0.2, balanced, width=width, color=colors[1], label=labels[0])
    plt.legend(prop={'size': 10}, loc='upper right')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Web Application')
    plt.ylim([0, 100])
    plt.xlim([0, 4])
    plt.yticks(y_ticks)
    plt.xticks(ticks=x, labels=x_ticks)
    plt.title('Anomaly Classifier Accuracy')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # classifier_type = 'mnb'
    # classifier_type = 'svm'
    # data = 'csic'
    # data = 'combined'
    # data = 'ecml'
    # data = 'outlier'
    # start_time = time.perf_counter()
    # train_classifier(classifier_type, data)
    # classify_requests(classifier_type, data)
    # end_time = time.perf_counter()
    # print(f'Time taken: {end_time - start_time} seconds')

    # csic_balanced, ecml_balanced, combined_balanced = get_results()
    # balanced_accuracies = pickle.load(open('balanced_accuracies.pkl', 'rb'))
    # csic_balanced, ecml_balanced, combined_balanced = balanced_accuracies['csic_balanced'], balanced_accuracies['ecml_balanced'], balanced_accuracies['combined_balanced']
    # plot_balanced(csic_balanced, ecml_balanced, combined_balanced)

    csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr = get_signature_results()
    # results = pickle.load(open('balanced_accuracies.pkl', 'rb'))
    # csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr = results['csic_tpr'], results['ecml_tpr'], results['combined_tpr'], results['csic_tnr'], results['ecml_tnr'], results['combined_tnr']
    # plot_tpr_tnr(csic_tpr, ecml_tpr, combined_tpr, csic_tnr, ecml_tnr, combined_tnr)

    # anomaly_balanced, anomaly_tpr, anomaly_tnr = get_anomaly_results()
    # results = pickle.load(open('svm_accuracies.pkl', 'rb'))
    # anomaly_balanced, anomaly_tpr, anomaly_tnr = results['balanced'], results['tpr'], results['tnr']
    # print(anomaly_balanced)
    # print(anomaly_tpr)
    # print(anomaly_tnr)
    
    # plot_anomaly(anomaly_balanced, anomaly_tpr, anomaly_tnr)