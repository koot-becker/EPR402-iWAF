# Existing imports
import csv
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Custom imports
import Classifiers.classifier_interface as classifier_interface

def train_classifier(classifier_type='mnb', dataset='csic', data=[], nu=0.5):
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

    classifier_interface.train_classifier(texts, labels, classifier_type, dataset, nu)
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

def test_anomaly_classifier(dataset_name='ctf', nu=0.5):
    data_path = f'Classifier/Datasets/GoBuster/{dataset_name}_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        training_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/{dataset_name}_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        testing_data = [row for row in reader]

    train_classifier(classifier_type='svm', dataset=dataset_name, data=training_data, nu=nu)

    return classify_requests(classifier_type='svm', dataset=dataset_name, data=testing_data)

def get_anomaly_results():
    tpr = []
    tnr = []
    balanced = []

    results = test_anomaly_classifier(dataset_name='ctf', nu=0.5)
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])

    results = test_anomaly_classifier(dataset_name='dvwa', nu=0.5)
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])

    results = test_anomaly_classifier(dataset_name='tiredful', nu=0.5)
    balanced.append(results[0])
    tpr.append(results[1])
    tnr.append(results[2])        
    
    with open('svm_accuracies_sim.pkl', 'wb') as f:
        pickle.dump({'balanced': balanced, 'tpr': tpr, 'tnr': tnr}, f)

    return balanced, tpr, tnr

def get_nu_results():
    ctf_tpr = []
    dvwa_tpr = []
    tiredful_tpr = []
    ctf_tnr = []
    dvwa_tnr = []
    tiredful_tnr = []
    ctf_balanced = []
    dvwa_balanced = []
    tiredful_balanced = []

    data_path = f'Classifier/Datasets/GoBuster/ctf_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        ctf_training_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/ctf_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        ctf_testing_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/dvwa_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        dvwa_training_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/dvwa_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        dvwa_testing_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/tiredful_training.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        tiredful_training_data = [row for row in reader]

    data_path = f'Classifier/Datasets/GoBuster/tiredful_testing.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        tiredful_testing_data = [row for row in reader]

    for i in range(1, 11, 1):
        print(f'Nu {i/10}:')
        results = test_anomaly_nu_classifier(nu=i/10, ctf_training_data=ctf_training_data, dvwa_training_data=dvwa_training_data, tiredful_training_data=tiredful_training_data, ctf_testing_data=ctf_testing_data, dvwa_testing_data=dvwa_testing_data, tiredful_testing_data=tiredful_testing_data)
        ctf_tpr.append(results[0])
        dvwa_tpr.append(results[1])
        tiredful_tpr.append(results[2])
        ctf_tnr.append(results[3])
        dvwa_tnr.append(results[4])
        tiredful_tnr.append(results[5])
        ctf_balanced.append(results[6])
        dvwa_balanced.append(results[7])
        tiredful_balanced.append(results[8])
    
    with open('nu_accuracies.pkl', 'wb') as f:
        pickle.dump({'ctf_tpr': ctf_tpr, 'dvwa_tpr': dvwa_tpr, 'tiredful_tpr': tiredful_tpr, 'ctf_tnr': ctf_tnr, 'dvwa_tnr': dvwa_tnr, 'tiredful_tnr': tiredful_tnr, 'ctf_balanced': ctf_balanced, 'dvwa_balanced': dvwa_balanced, 'tiredful_balanced': tiredful_balanced}, f)

    return ctf_tpr, dvwa_tpr, tiredful_tpr, ctf_tnr, dvwa_tnr, tiredful_tnr, ctf_balanced, dvwa_balanced, tiredful_balanced

def test_anomaly_nu_classifier(nu=0.1, ctf_training_data=[], dvwa_training_data=[], tiredful_training_data=[], ctf_testing_data=[], dvwa_testing_data=[], tiredful_testing_data=[]):
    # CTF
    train_classifier(classifier_type='svm', dataset='ctf', data=ctf_training_data, nu=nu)
    ctf_balanced, ctf_tpr, ctf_tnr = classify_requests(classifier_type='svm', dataset='ctf', data=ctf_testing_data)

    # DVWA
    train_classifier(classifier_type='svm', dataset='dvwa', data=dvwa_training_data, nu=nu)
    dvwa_balanced, dvwa_tpr, dvwa_tnr = classify_requests(classifier_type='svm', dataset='dvwa', data=dvwa_testing_data)

    # TIREDFUL
    train_classifier(classifier_type='svm', dataset='tiredful', data=tiredful_training_data, nu=nu)
    tiredful_balanced, tiredful_tpr, tiredful_tnr = classify_requests(classifier_type='svm', dataset='tiredful', data=tiredful_testing_data)

    return ctf_tpr, dvwa_tpr, tiredful_tpr, ctf_tnr, dvwa_tnr, tiredful_tnr, ctf_balanced, dvwa_balanced, tiredful_balanced

def get_mnb_svm(svm_tpr, svm_tnr, mnb_tpr, mnb_tnr):
    tpr_avg = np.mean(mnb_tpr)
    tnr_avg = np.mean(mnb_tnr)

    tnr_combined = (3*tnr_avg + [x for x in svm_tnr]) / 4
    tpr_combined = (3*tpr_avg + [x for x in svm_tpr]) / 4

    return tnr_combined, tpr_combined

def plot_nu(tpr, tnr, balanced, dataset='CSIC'):
    x = np.arange(0.1, 1.1, 0.1)
    width = 0.03
    y_ticks = np.arange(0, 110, 10)
    labels = ['TPR', 'TNR', 'Balanced']
    colors = ['red', 'lime', 'tan']

    plt.bar(x - width, tpr, width=width, color=colors[0], label=labels[0])
    plt.bar(x, tnr, width=width, color=colors[1], label=labels[1])
    plt.bar(x + width, balanced, width=width, color=colors[2], label=labels[2])
    plt.legend(prop={'size': 10}, loc='upper right')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Nu Value')
    plt.ylim([0, 100])
    plt.xlim([0, 1.1])
    plt.yticks(y_ticks)
    plt.xticks(x)
    plt.grid(axis='y')
    plt.title(f'Classifier Accuracy - {dataset}')

    plt.tight_layout()
    plt.show()

def get_metrics(tpr, tnr):
    accuracy = [(tp + tn) / (tp + tn + fp + fn) for tp, tn, fp, fn in zip(tpr, tnr, [100 - x for x in tpr], [100 - x for x in tnr])]
    precision = [tp / (tp + fp) for tp, fp in zip(tpr, [100 - x for x in tnr])]
    recall = [tp / (tp + fn) for tp, fn in zip(tpr, [100 - x for x in tpr])]
    specificity = [tn / (tn + fp) for tn, fp in zip(tnr, [100 - x for x in tnr])]
    f1 = [2 * ((p * r) / (p + r)) for p, r in zip(precision, recall)]

    return accuracy, precision, recall, specificity, f1

def plot_anomaly_metrics(tpr, tnr):
    accuracy, precision, recall, specificity, f1 = get_metrics(tpr, tnr)

    print(f'Accuracy: {accuracy}')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'Specificity: {specificity}')
    print(f'F1: {f1}')

    x = np.arange(1, 4, 1)
    width = 0.15
    y_ticks = np.arange(0, 1.1, 0.1)
    x_ticks = ['CTF-JWT', 'DVWA', 'TIREDFUL']
    labels = ['Accuracy', 'Precision', 'Recall', 'Specificity', 'F1']
    colors = ['red', 'tan', 'lime', 'blue', 'purple']

    plt.bar(x - 0.3, accuracy, width=width, color=colors[0], label=labels[0])
    plt.bar(x - 0.15, precision, width=width, color=colors[1], label=labels[1])
    plt.bar(x, recall, width=width, color=colors[2], label=labels[2])
    plt.bar(x + 0.15, specificity, width=width, color=colors[3], label=labels[3])
    plt.bar(x + 0.3, f1, width=width, color=colors[4], label=labels[4])
    plt.legend(prop={'size': 10}, loc='upper right')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Dataset')
    plt.ylim([0, 1])
    plt.xlim([0, 4])
    plt.yticks(y_ticks)
    plt.xticks(x, labels=x_ticks)
    plt.grid(axis='y')
    plt.title(f'SVM Classifier Metrics')

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
    plt.grid(axis='y')
    plt.title('Anomaly Classifier Accuracy')
    
    plt.tight_layout()
    plt.show()

def plot_mnb_svm(svm_balanced, svm_tpr, svm_tnr, mnb_balanced, mnb_tpr, mnb_tnr):
    x = np.arange(1, 4, 1)
    width = 0.2
    y_ticks = np.arange(0, 110, 10)
    x_ticks = ['CTF-JWT', 'DVWA', 'TIREDFUL']

    colors = ['red', 'tan', 'lime']
    labels = ['Balanced', 'TPR', 'TNR']

    tpr_avg = np.mean(mnb_tpr)
    tnr_avg = np.mean(mnb_tnr)
    balanced_avg = np.mean(mnb_balanced)

    tnr_combined = (3*tnr_avg + [x for x in svm_tnr]) / 4
    tpr_combined = (3*tpr_avg + [x for x in svm_tpr]) / 4
    balanced_combined = (3*balanced_avg + [x for x in svm_balanced]) / 4

    print(f'TNR: {tnr_combined}')
    print(f'TPR: {tpr_combined}')
    print(f'Balanced: {balanced_combined}')

    plt.bar(x - 0.2, tnr_combined, width=width, color=colors[0], label=labels[2])
    plt.bar(x, tpr_combined, width=width, color=colors[2], label=labels[1])
    plt.bar(x + 0.2, balanced_combined, width=width, color=colors[1], label=labels[0])
    plt.legend(prop={'size': 10}, loc='upper right')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Web Application')
    plt.ylim([0, 100])
    plt.xlim([0, 4])
    plt.yticks(y_ticks)
    plt.xticks(ticks=x, labels=x_ticks)
    plt.grid(axis='y')
    plt.title('Overall Combined Balanced Accuracy')
    
    plt.tight_layout()
    plt.show()

    return

if __name__ == "__main__":
    # classifier_type = 'svm'
    # data = 'outlier'
    # start_time = time.perf_counter()
    # end_time = time.perf_counter()
    # print(f'Time taken: {end_time - start_time} seconds')

    '''Support Vector Machine Classifier'''
    # anomaly_balanced, anomaly_tpr, anomaly_tnr = get_anomaly_results()
    # results = pickle.load(open('svm_accuracies_sim.pkl', 'rb'))
    # anomaly_balanced, anomaly_tpr, anomaly_tnr = results['balanced'], results['tpr'], results['tnr']
    
    # plot_anomaly(anomaly_balanced, anomaly_tpr, anomaly_tnr)

    # plot_anomaly_metrics(anomaly_tpr, anomaly_tnr)

    # ctf_balanced, ctf_tpr, ctf_tnr, dvwa_balanced, dvwa_tpr, dvwa_tnr, tiredful_balanced, tiredful_tpr, tiredful_tnr = get_nu_results()
    # results = pickle.load(open('nu_accuracies.pkl', 'rb'))
    # ctf_balanced, ctf_tpr, ctf_tnr = results['ctf_balanced'], results['ctf_tpr'], results['ctf_tnr']
    # dvwa_balanced, dvwa_tpr, dvwa_tnr = results['dvwa_balanced'], results['dvwa_tpr'], results['dvwa_tnr']
    # tiredful_balanced, tiredful_tpr, tiredful_tnr = results['tiredful_balanced'], results['tiredful_tpr'], results['tiredful_tnr']
    # plot_nu(ctf_tpr, ctf_tnr, ctf_balanced, 'CTF-JWT')
    # plot_nu(dvwa_tpr, dvwa_tnr, dvwa_balanced, 'DVWA')
    # plot_nu(tiredful_tpr, tiredful_tnr, tiredful_balanced, 'TIREDFUL')

    # csic_results = pickle.load(open('balanced_accuracies_csic.pkl', 'rb'))
    # csic_tpr, csic_tnr, csic_balanced = csic_results['csic_tpr'], csic_results['csic_tnr'], csic_results['csic_balanced']
    # plot_mnb_svm(csic_balanced, csic_tpr, csic_tnr, anomaly_balanced, anomaly_tpr, anomaly_tnr)
    # tnr, tpr = get_mnb_svm(anomaly_tpr, anomaly_tnr, csic_tpr, csic_tnr)
    # plot_anomaly_metrics(tpr, tnr)
    
    balanced, tpr, tnr = test_anomaly_classifier(dataset_name='ctf', nu=0.5)
    print(f'Balanced: {balanced}, TPR: {tpr}, TNR: {tnr}')