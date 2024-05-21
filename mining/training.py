import json
import tensorflow as tf
# from sklearn.model_selection import train_test_split

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
    # Extract relevant features and labels
    features = []
    track = []
    start = []
    result = []
    horse = []
    trainer = []
    labels = []
    for horseData in data:
        races = horseData['races']
        for race in races:
            raceResult = race['result']
            raceTrack = race['track']
            raceStarts = race['starts']

            features.append([
                race['distance'],
                race['startMethod'],
                race['sport'],

            ])

            result.append([
                raceResult['victoryMargin'],
                raceResult['scratchings'],
            ])

            track.append([
                raceTrack['name'],
                raceTrack['condition'],
                raceTrack['countryCode'],
            ])

            for raceStart in raceStarts:

                horseStart = raceStart['horse']
                record = horseStart['record']
                recordTime = record['time']
                horseTrainer = horseStart['trainer']
                trainerHomeTrack = horseTrainer['homeTrack']
                trainerStatistics = horseTrainer['statistics']
                trainerIsolatedStatistics = []
                trainerIsolatedStatistics.append([
                    trainerStatistics['years'],
                ])
                trainerIsolatedHomeTrack = []
                trainerIsolatedHomeTrack.append([
                    trainerHomeTrack['name']
                ])

                trainer.append([
                    horseTrainer['firstName'],
                    horseTrainer['lastName'],
                    horseTrainer['location'],
                    horseTrainer['birth'],
                    horseTrainer['license'],
                ])

                horse.append([
                    horseStart['name'],
                    horseStart['age'],
                    horseStart['sex'],
                    record['code'],
                    record['startMethod'],
                    record['distance'],
                    recordTime['minutes'],
                    recordTime['seconds'],
                    recordTime['tenths'],
                ])

                start.append([
                    raceStart['number'],
                    raceStart['postPosition'],
                ])

    return features, track, labels


# Load the data
data = load_data('results.json')
features, track, labels = preprocess_data(data)

print(features)

# Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
#
# # Create a TensorFlow dataset
# train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(32)
# test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32)

# Define the model
# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(64, activation='relu', input_shape=(len(features[0]),)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(1)  # Assuming we are predicting a single continuous value
# ])
#
# # Compile the model
# model.compile(optimizer='adam',
#               loss='mean_squared_error',  # Adjust loss function as needed
#               metrics=['mean_absolute_error'])
#
# # Train the model
# model.fit(train_dataset, epochs=10)
#
# # Evaluate the model
# model.evaluate(test_dataset)
#
# # Save the model
# model.save('horse_racing_model.h5')
#
# print("Model training and evaluation complete.")
