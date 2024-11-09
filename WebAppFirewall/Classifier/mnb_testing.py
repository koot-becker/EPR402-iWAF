# Existing imports
import csv
import threading
import matplotlib.pyplot as plt
import numpy as np
import pickle
import seaborn as sns

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
    valid_data = valid_data[:int(len(valid_data))]
    anomalous_data = anomalous_data[:int(len(anomalous_data))]

    # Create the split point
    valid_split_point = int(len(valid_data) * (training_ratio / 100))
    anomalous_split_point = int(len(anomalous_data) * (training_ratio / 100))


    # Split the data
    training_data = valid_data[:valid_split_point] + anomalous_data[:anomalous_split_point]
    testing_data = valid_data[valid_split_point:] + anomalous_data[anomalous_split_point:]

    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/Split/{dataset}_testing.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=testing_data[0].keys())
        writer.writeheader()
        writer.writerows(testing_data)

    return training_data, testing_data

def train_classifier(classifier_type='mnb', dataset='csic', data=[], alpha=1.0):
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

    classifier_interface.train_classifier(texts, labels, classifier_type, dataset, alpha)
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
        if count % 100 == 0:
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

def test_signature_classifier(split=90):  
    # CSIC
    # csic_data = split_dataset(dataset='csic', training_ratio=split)
    with open(f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/Split/csic_testing.csv', 'r') as file:
        reader = csv.DictReader(file)
        csic_data = [row for row in reader]
    # train_classifier(classifier_type='mnb', dataset='csic', data=csic_data[0])
    print('CSIC Testing')
    csic_balanced, csic_tpr, csic_tnr = classify_requests(classifier_type='mnb', dataset='csic', data=csic_data)

    return csic_tpr, csic_tnr, csic_balanced

def get_signature_results():
    csic_tpr = []
    csic_tnr = []
    csic_balanced = []
    for i in range(1, 21, 1):
        print(f'Round {i}:')
        results = test_signature_classifier(split=90)
        csic_tpr.append(results[0])
        csic_tnr.append(results[1])
        csic_balanced.append(results[2])

        with open(f'balanced_accuracies_csic_{i}_sim.pkl', 'wb') as f:
            pickle.dump({'csic_tpr': results[0], 'csic_tnr': results[1], 'csic_balanced': results[2]}, f)

    with open('balanced_accuracies_csic_sim.pkl', 'wb') as f:
        pickle.dump({'csic_tpr': csic_tpr, 'csic_tnr': csic_tnr, 'csic_balanced': csic_balanced}, f)

    return

def get_metrics(tpr, tnr):
    accuracy = [(tp + tn) / (tp + tn + fp + fn) for tp, tn, fp, fn in zip(tpr, tnr, [100 - x for x in tpr], [100 - x for x in tnr])]
    precision = [tp / (tp + fp) for tp, fp in zip(tpr, [100 - x for x in tnr])]
    recall = [tp / (tp + fn) for tp, fn in zip(tpr, [100 - x for x in tpr])]
    specificity = [tn / (tn + fp) for tn, fp in zip(tnr, [100 - x for x in tnr])]
    f1 = [2 * ((p * r) / (p + r)) for p, r in zip(precision, recall)]

    return accuracy, precision, recall, specificity, f1

def get_alpha_results():
    csic_tpr = []
    csic_tnr = []
    csic_balanced = []
    csic_data = split_dataset(dataset='csic', training_ratio=1)
    for i in np.arange(0.01, 1.01, 0.01):
        print(f'Round {i}:')
        results = test_signature_alpha_classifier(alpha=i, csic_data=csic_data)
        csic_tpr.append(results[0])
        csic_tnr.append(results[3])
        csic_balanced.append(results[6])

    with open('alpha_accuracies_sim.pkl', 'wb') as f:
        pickle.dump({'csic_tpr': csic_tpr, 'csic_tnr': csic_tnr, 'csic_balanced': csic_balanced}, f)

    return csic_tpr, csic_tnr, csic_balanced

def test_signature_alpha_classifier(alpha=1.0, csic_data=[]):

    # CSIC
    train_classifier(classifier_type='mnb', dataset='csic', data=csic_data[0], alpha=alpha)
    csic_balanced, csic_tpr, csic_tnr = classify_requests(classifier_type='mnb', dataset='csic', data=csic_data[1])

    return csic_tpr, csic_tnr, csic_balanced

def plot_alpha(tpr, tnr, balanced, dataset='CSIC'):
    x = np.arange(0.01, 1.01, 0.01)
    width = 0.005
    y_ticks = np.arange(0, 101, 10)
    x_ticks = np.arange(0, 1.01, 0.1)
    labels = ['TPR', 'TNR', 'Balanced']
    colors = ['red', 'lime', 'tan']

    fig, axs = plt.subplots(3, 1, figsize=(5, 10))

    axs[0].bar(x, tpr, width=width, color=colors[0], label=labels[0])
    axs[0].legend(prop={'size': 10}, loc='upper right')
    axs[0].set_ylabel('Accuracy (%)')
    axs[0].set_xlabel('Alpha Value')
    axs[0].set_ylim([0, 100])
    axs[0].set_xlim([0, 1.01])
    axs[0].set_yticks(y_ticks)
    axs[0].set_xticks(x_ticks)
    axs[0].set_title(f'True Positive Rate - {dataset}')

    axs[1].bar(x, tnr, width=width, color=colors[1], label=labels[1])
    axs[1].legend(prop={'size': 10}, loc='upper right')
    axs[1].set_ylabel('Accuracy (%)')
    axs[1].set_xlabel('Alpha Value')
    axs[1].set_ylim([0, 100])
    axs[1].set_xlim([0, 1.01])
    axs[1].set_yticks(y_ticks)
    axs[1].set_xticks(x_ticks)
    axs[1].set_title(f'True Negative Rate - {dataset}')

    axs[2].bar(x, balanced, width=width, color=colors[2], label=labels[2])
    axs[2].legend(prop={'size': 10}, loc='upper right')
    axs[2].set_ylabel('Accuracy (%)')
    axs[2].set_xlabel('Alpha Value')
    axs[2].set_ylim([0, 100])
    axs[2].set_xlim([0, 1.01])
    axs[2].set_yticks(y_ticks)
    axs[2].set_xticks(x_ticks)
    axs[2].set_title(f'Balanced Accuracy - {dataset}')

    plt.tight_layout()
    plt.show()

def get_statistics(data):
    mean = np.mean(data)
    std = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)
    med = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    rng = max_val - min_val
    skewness = 3 * (mean - med) / std

    return {'Mean': mean, 'Standard Deviation': std, 'Minimum': min_val, 'Maximum': max_val, 'Median': med, 'Q1': q1, 'Q3': q3, 'IQR': iqr, 'Range': rng, 'Skewness': skewness}

def plot_metrics(accuracy, precision, recall, specificity, f1, dataset='CSIC'):
    x = np.arange(1, 101, 1)
    width = 0.8
    y_ticks = np.arange(0, 1.1, 0.1)
    x_ticks = np.arange(10, 101, 10)
    labels = ['Accuracy', 'Precision', 'Recall', 'Specificity', 'F1']
    colors = ['red', 'tan', 'lime', 'blue', 'purple']

    fig, axs = plt.subplots(5, 1, figsize=(5, 10))

    axs[0].bar(x, accuracy, width=width, color=colors[0], label=labels[0])
    axs[0].axhline(y=np.mean(accuracy), color='black', linestyle='--', linewidth=1, label='Mean')
    axs[0].legend(prop={'size': 10}, loc='upper right')
    axs[0].set_ylabel('Accuracy (%)')
    axs[0].set_ylim([0, 1])
    axs[0].set_xlim([0, 101])
    axs[0].set_yticks(y_ticks)
    axs[0].set_xticks(x_ticks)
    axs[0].set_xlabel('Run Number')
    axs[0].grid(axis='y')
    axs[0].set_title(f'{dataset} Classifier Accuracy')

    axs[1].bar(x, precision, width=width, color=colors[1], label=labels[1])
    axs[1].axhline(y=np.mean(precision), color='black', linestyle='--', linewidth=1, label='Mean')
    axs[1].legend(prop={'size': 10}, loc='upper right')
    axs[1].set_ylabel('Precision (%)')
    axs[1].set_ylim([0, 1])
    axs[1].set_xlim([0, 101])
    axs[1].set_yticks(y_ticks)
    axs[1].set_xticks(x_ticks)
    axs[1].set_xlabel('Run Number')
    axs[1].grid(axis='y')
    axs[1].set_title(f'{dataset} Classifier Precision')

    axs[2].bar(x, recall, width=width, color=colors[2], label=labels[2])
    axs[2].axhline(y=np.mean(recall), color='black', linestyle='--', linewidth=1, label='Mean')
    axs[2].legend(prop={'size': 10}, loc='upper right')
    axs[2].set_ylabel('Recall (%)')
    axs[2].set_ylim([0, 1])
    axs[2].set_xlim([0, 101])
    axs[2].set_yticks(y_ticks)
    axs[2].set_xticks(x_ticks)
    axs[2].set_xlabel('Run Number')
    axs[2].grid(axis='y')
    axs[2].set_title(f'{dataset} Classifier Recall')

    axs[3].bar(x, specificity, width=width, color=colors[3], label=labels[3])
    axs[3].axhline(y=np.mean(specificity), color='black', linestyle='--', linewidth=1, label='Mean')
    axs[3].legend(prop={'size': 10}, loc='upper right')
    axs[3].set_ylabel('Specificity (%)')
    axs[3].set_ylim([0, 1])
    axs[3].set_xlim([0, 101])
    axs[3].set_yticks(y_ticks)
    axs[3].set_xticks(x_ticks)
    axs[3].set_xlabel('Run Number')
    axs[3].grid(axis='y')
    axs[3].set_title(f'{dataset} Classifier Specificity')

    axs[4].bar(x, f1, width=width, color=colors[4], label=labels[4])
    axs[4].axhline(y=np.mean(f1), color='black', linestyle='--', linewidth=1, label='Mean')
    axs[4].legend(prop={'size': 10}, loc='upper right')
    axs[4].set_ylabel('F1 Score (%)')
    axs[4].set_ylim([0, 1])
    axs[4].set_xlim([0, 101])
    axs[4].set_yticks(y_ticks)
    axs[4].set_xticks(x_ticks)
    axs[4].set_xlabel('Run Number')
    axs[4].grid(axis='y')
    axs[4].set_title(f'{dataset} Classifier F1 Score')

    plt.tight_layout()
    plt.show()

def plot_statistics(accuracy, precision, recall, specificity, f1, dataset='CSIC'):
    print(f'Accuracy Stats: {get_statistics(accuracy)}\n')
    print(f'Precision Stats: {get_statistics(precision)}\n')
    print(f'Recall Stats: {get_statistics(recall)}\n')
    print(f'Specificity Stats: {get_statistics(specificity)}\n')
    print(f'F1 Stats: {get_statistics(f1)}\n')

    fig, axs = plt.subplots(1, 5, figsize=(10, 5))
    metrics = ['Accuracy', 'Precision', 'Recall', 'Specificity', 'F1']
    data = [accuracy, precision, recall, specificity, f1]
    
    for i, ax in enumerate(axs):
        sns.boxplot(data=data[i], orient='v', color='blue', ax=ax)
        ax.set_yticks(np.arange(0.9, 1.01, 0.01))
        ax.set_ylim([0.9, 1.0])
        ax.set_title(f'{metrics[i]}')

    fig.suptitle(f'{dataset} Classifier Statistics', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_combined(tpr, tnr, balanced, dataset='CSIC'):
    x = np.arange(1, 11, 1)
    width = 0.8
    y_ticks = np.arange(0, 101, 10)
    x_ticks = np.arange(1, 11, 1)

    colors = ['red', 'lime', 'tan']
    labels = ['TNR', 'TPR', 'Balanced']

    fig, axs = plt.subplots(3, 1, figsize=(5, 10))
    tnr_max = max(tnr)
    tpr_max = max(tpr)
    balanced_max = max(balanced)
    tpr_avg = np.mean(tpr)
    tnr_avg = np.mean(tnr)
    balanced_avg = np.mean(balanced)
    tpr_min = min(tpr)
    tnr_min = min(tnr)
    balanced_min = min(balanced)

    axs[0].bar(x, tnr, width=width, color=colors[0], label=labels[0])
    axs[0].axhline(y=tnr_max, color='black', linestyle='--', linewidth=1, label=f'Max - {tnr_max:.2f}')
    axs[0].axhline(y=tnr_avg, color='black', linestyle='--', linewidth=1, label=f'Mean - {tnr_avg:.2f}')
    axs[0].axhline(y=tnr_min, color='black', linestyle='--', linewidth=1, label=f'Min - {tnr_min:.2f}')
    axs[0].legend(prop={'size': 10}, loc='lower right')
    axs[0].set_ylabel('Accuracy (%)')
    axs[0].set_xlabel('Simulation Run Number')
    axs[0].set_ylim([0, 100])
    axs[0].set_xlim([0, 11])
    axs[0].set_yticks(y_ticks)
    axs[0].set_xticks(x_ticks)
    axs[0].set_title(f'Signature Classifier TNR - {dataset}')

    axs[1].bar(x, tpr, width=width, color=colors[1], label=labels[1])
    axs[1].axhline(y=tpr_max, color='black', linestyle='--', linewidth=1, label=f'Max - {tpr_max:.2f}')
    axs[1].axhline(y=tpr_avg, color='black', linestyle='--', linewidth=1, label=f'Average - {tpr_avg:.2f}')
    axs[1].axhline(y=tpr_min, color='black', linestyle='--', linewidth=1, label=f'Min - {tpr_min:.2f}')
    axs[1].legend(prop={'size': 10}, loc='lower right')
    axs[1].set_ylabel('Accuracy (%)')
    axs[1].set_xlabel('Simulation Run Number')
    axs[1].set_ylim([0, 100])
    axs[1].set_xlim([0, 11])
    axs[1].set_yticks(y_ticks)
    axs[1].set_xticks(x_ticks)
    axs[1].set_title(f'Signature Classifier TPR - {dataset}')

    axs[2].bar(x, balanced, width=width, color=colors[2], label=labels[2])
    axs[2].axhline(y=balanced_max, color='black', linestyle='--', linewidth=1, label=f'Max - {balanced_max:.2f}')
    axs[2].axhline(y=balanced_avg, color='black', linestyle='--', linewidth=1, label=f'Average - {balanced_avg:.2f}')
    axs[2].axhline(y=balanced_min, color='black', linestyle='--', linewidth=1, label=f'Min - {balanced_min:.2f}')
    axs[2].legend(prop={'size': 10}, loc='lower right')
    axs[2].set_ylabel('Accuracy (%)')
    axs[2].set_xlabel('Simulation Run Number')
    axs[2].set_ylim([0, 100])
    axs[2].set_xlim([0, 11])
    axs[2].set_yticks(y_ticks)
    axs[2].set_xticks(x_ticks)
    axs[2].set_title(f'Signature Classifier Balanced Accuracy - {dataset}')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    '''Multinomial Naive Bayes Classifier'''
    # Signature Results
    # get_signature_results()
    # results = pickle.load(open('balanced_accuracies_csic.pkl', 'rb'))
    # csic_tpr, csic_tnr, csic_balanced = results['csic_tpr'], results['csic_tnr'], results['csic_balanced']
    # plot_combined(csic_tpr, csic_tnr, csic_balanced, 'CSIC')

    # Metric Results
    # csic_accuracy, csic_precision, csic_recall, csic_specificity, csic_f1 = get_metrics(csic_tpr, csic_tnr)
    # plot_metrics(csic_accuracy, csic_precision, csic_recall, csic_specificity, csic_f1, 'CSIC')
    # plot_statistics(csic_accuracy, csic_precision, csic_recall, csic_specificity, csic_f1, 'CSIC')

    # Alpha Results
    # csic_tpr, csic_tnr, csic_balanced, = get_alpha_results()
    # results = pickle.load(open('alpha_accuracies_sim.pkl', 'rb'))
    # csic_tpr, csic_tnr, csic_balanced = results['csic_tpr'], results['csic_tnr'], results['csic_balanced']
    # plot_alpha(csic_tpr, csic_tnr, csic_balanced, 'CSIC')

    tpr, tnr, balanced = test_signature_classifier(split=95)
    print(f'TPR: {tpr}, TNR: {tnr}, Balanced: {balanced}')
    