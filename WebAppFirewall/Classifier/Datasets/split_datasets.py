import csv
import random

def split_dataset(dataset, training_ratio=10):
    # Load the data
    data_path = f'/home/dieswartkat/EPR402/WebAppFirewall/Classifier/Datasets/Original/{dataset}.csv'
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Prepare the training data
    labels = [row['Class'] for row in data]

    # Split the data
    valid_data = [row for row in data if row['Class'] == 'Valid']
    anomalous_data = [row for row in data if row['Class'] == 'Anomalous']

    # Create the split point
    valid_split_point = int(len(valid_data) * (training_ratio / 100))
    anomalous_split_point = int(len(anomalous_data) * (training_ratio / 100))

    # Shuffle the data
    random.shuffle(valid_data)
    random.shuffle(anomalous_data)

    # Split the data
    training_data = valid_data[:valid_split_point] + anomalous_data[:anomalous_split_point]
    testing_data = valid_data[valid_split_point:] + anomalous_data[anomalous_split_point:]

    # Save the split datasets
    with open(f'{dataset}_training_{training_ratio}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(training_data)

    with open(f'{dataset}_testing_{training_ratio}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(testing_data)

    print('Datasets saved successfully.')

if __name__ == "__main__":
    split_dataset(dataset='csic', training_ratio=90)