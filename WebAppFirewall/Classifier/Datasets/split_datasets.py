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

# Create the split point
split_point = int(len(valid_data) * 0.8)

# Shuffle the data
random.shuffle(valid_data)

# Split the data
valid_training_data = valid_data[:split_point]
valid_testing_data = valid_data[split_point:]

# Save the split datasets
with open('training.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(valid_training_data)

with open('testing_valid.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(valid_testing_data)

print('Datasets saved successfully.')