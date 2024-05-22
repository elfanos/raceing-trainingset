import json
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Description: This file contains the training function for the model


def my_function():
    print("Hello from a function")


my_function()

# Load and process the JSON data


def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def preprocess_data(data):
    features = []
    labels = []

    for horseData in data:
        races = horseData['races']
        for race in races:
            raceResult = race['result']
            raceTrack = race['track']
            raceStarts = race['starts']

            for raceStart in raceStarts:
                horseStart = raceStart['horse']
                record = horseStart['record']
                recordTime = record['time']
                horseTrainer = horseStart['trainer']
                trainerHomeTrack = horseTrainer['homeTrack']
                trainerStatistics = horseTrainer['statistics']

                # Extract features
                features.append([
                    race['distance'],
                    race['startMethod'],
                    race['sport'],
                    horseStart['age'],
                    horseStart['money'],
                    horseStart['statistics']['years']['2024']['starts'],
                    horseStart['statistics']['years']['2024']['earnings'],
                    horseStart['statistics']['years']['2024']['placement']['1'],
                    horseStart['statistics']['years']['2024']['placement']['2'],
                    horseStart['statistics']['years']['2024']['placement']['3'],
                    raceStart['number'],
                    raceStart['postPosition'],
                    recordTime['minutes'],
                    recordTime['seconds'],
                    recordTime['tenths'],
                    raceTrack['condition'],
                    raceTrack['countryCode'],
                    horseTrainer['firstName'],
                    horseTrainer['lastName'],
                    horseTrainer['location'],
                    horseTrainer['birth'],
                    horseTrainer['license'],
                    trainerHomeTrack['name'],
                    trainerStatistics['years']['2024']['starts'],
                    trainerStatistics['years']['2024']['earnings'],
                    trainerStatistics['years']['2024']['placement']['1'],
                    trainerStatistics['years']['2024']['placement']['2'],
                    trainerStatistics['years']['2024']['placement']['3']
                ])

                # Extract labels
                # labels.append(raceResult['place'])

    return features, labels


# Load the data
data = load_data('results.json')
features, labels = preprocess_data(data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42)

# Create a TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices(
    (X_train, y_train)).batch(32)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32)
# Define the model



# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(64, activation='relu',
#                           input_shape=(len(features[0]),)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     # Assuming we are predicting a single continuous value
#     tf.keras.layers.Dense(1)
# ])
#
# # Compile the model
# model.compile(optimizer='adam',
#               loss='mean_squared_error',  # Adjust loss function as needed
#               metrics=['mean_absolute_error'])
#
# # Train the model
model.fit(train_dataset, epochs=10)
#
# # Evaluate the model
model.evaluate(test_dataset
#
# # Save the model
# model.save('horse_racing_model.h5')
#
# print("Model training and evaluation complete.")
