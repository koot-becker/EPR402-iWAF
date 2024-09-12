import csv
import random

# Load the data
data_path = '/home/administrator/EPR402/WebAppFirewall/Classifier/Datasets/CSVData/csic_ecml_final.csv'
with open(data_path, 'r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Prepare the training data
labels = [row['Class'] for row in data]

# Split the data
valid_data = [row for row in data if row['Class'] == 'Valid']
anomalous_data = [row for row in data if row['Class'] == 'Anomalous']

# Shuffle the data
random.shuffle(valid_data)
random.shuffle(anomalous_data)

# Determine the split point
split_point_valid = int(len(valid_data) * 0.8)
split_point_anomalous = int(len(anomalous_data) * 0.8)

# Split the data
dataset1 = valid_data[:split_point_valid] + anomalous_data[:split_point_anomalous]
dataset2 = valid_data[split_point_valid:] + anomalous_data[split_point_anomalous:]

# Save the split datasets
with open('/home/administrator/EPR402/WebAppFirewall/Classifier/Datasets/combined_training.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(dataset1)

with open('/home/administrator/EPR402/WebAppFirewall/Classifier/Datasets/combined_testing.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(dataset2)

print('Datasets saved successfully.')