import csv
import random

# Load the data
data_path = 'csic_testing.csv'
with open(data_path, 'r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Prepare the training data
labels = [row['Class'] for row in data]

# Split the data
valid_data = [row for row in data if row['Class'] == 'Valid']
anomalous_data = [row for row in data if row['Class'] == 'Anomalous']

# Create the split point
valid_split_point = int(len(valid_data) * 0.01)

# Shuffle the data
random.shuffle(valid_data)
random.shuffle(anomalous_data)

# Split the data
valid_training_data = valid_data[:valid_split_point]
valid_testing_data = valid_data[valid_split_point:] + anomalous_data

# Save the split datasets
with open('training_outlier.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(valid_training_data)

with open('testing_outlier.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(valid_testing_data)

print('Datasets saved successfully.')