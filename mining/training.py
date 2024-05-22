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
    track = []
    start = []
    labels = []
    for horseData in data:
        races = horseData['races']
        for race in races:
            raceResult = race['result']
            raceTrack = race['track']
            raceStarts = race['starts']

            # raceData
            raceData = []
            raceData.append([
                race['distance'],
                race['startMethod'],
                race['sport'],
            ])
            # resultData
            resultData = []
            resultData.append([
                raceResult['victoryMargin'],
                raceResult['scratchings'],
            ])

            # Track data
            trackData = []
            trackData.append([
                raceTrack['name'],
                raceTrack['condition'],
                raceTrack['countryCode'],
            ])

            for raceStart in raceStarts:

                horseStart = raceStart['horse']
                record = horseStart['record']
                recordTime = record['time']

                # Trainer
                horseTrainer = horseStart['trainer']
                horseTrainerHomeTrack = horseTrainer['homeTrack']
                trainerHomeTrack = []
                trainerHomeTrack.append([])

                trainerStatistics = horseTrainer['statistics']
                trainerStatistic = []
                trainerStatistic.append([
                    trainerStatistics['years'],
                ])
                trainer = []
                trainer.append([
                    horseTrainer['firstName'],
                    horseTrainer['lastName'],
                    horseTrainer['location'],
                    horseTrainer['birth'],
                    horseTrainer['license'],
                ])

                # Horse
                horse = []
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
                # start
                start.append([
                    raceStart['number'],
                    raceStart['postPosition'],
                ])
                # create data set as array
                features.append(start)
                features.append(horse)
                features.append(trainer)
                features.append(trainerStatistic)
                features.append(trainerHomeTrack)
                features.append(trackData)

    return features, track, labels


# Load the data
data = load_data('results.json')
features, track, labels = preprocess_data(data)
print(features)
