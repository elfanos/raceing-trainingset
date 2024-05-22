
import json
from math import isnan
import numpy as np
import matplotlib.pyplot as plt
from optree import PyTree
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import pandas as pd
import keras as kr

from statistic import static_dataset_columns, statistic_dataset


def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def race_data(data):
    features = []
    columns = []

    # start
    columns.extend(['start_number', 'start_postPosition'])

    columns.extend([
        'horse_record_minutes', 'horse_record_seconds', 'horse_record_tenths'])

    columns.extend(static_dataset_columns('horse_stats_year_2023'))
    columns.extend(static_dataset_columns('horse_stats_year_2024'))

    columns.extend(static_dataset_columns('horse_trainer_stats_year_2023'))
    columns.extend(static_dataset_columns('horse_trainer_stats_year_2024'))
    columns.extend(['horse_placement'])

    for horseData in data:
        races = horseData['races']
        for race in races:
            raceResult = race['result']
            raceStarts = race['starts']

            for raceStart in raceStarts:
                features_vector = []

                horseStart = raceStart['horse']
                record = horseStart['record']
                recordTime = record['time']
                raceResult = raceStart['result']

                # start
                start = []
                start.append([
                    raceStart['number'],
                    raceStart['postPosition'],
                ])

                # Trainer
                horseTrainer = horseStart['trainer']

                # Horse
                horse = []
                horse.append([
                    recordTime['minutes'],
                    recordTime['seconds'],
                    recordTime['tenths'],
                ])

                # create data set as array
                features_vector.extend(start)
                features_vector.extend(horse)

                # horse stats
                horseStat = horseStart['statistics']['years']
                if (horseStat is not None):
                    if (horseStat.get('2023') is not None):
                        horse_stats_year_2023 = horseStat['2023']

                        features_vector.append([
                            horse_stats_year_2023["starts"],
                            horse_stats_year_2023["earnings"],
                            horse_stats_year_2023["placement"]["1"],
                            horse_stats_year_2023["placement"]["2"],
                            horse_stats_year_2023["placement"]["3"],
                            horse_stats_year_2023["winPercentage"],
                        ])

                    if (horseStat.get('2024') is not None):
                        horse_stats_year_2024 = horseStat['2024']
                        features_vector.append([
                            horse_stats_year_2024["starts"],
                            horse_stats_year_2024["earnings"],
                            horse_stats_year_2024["placement"]["1"],
                            horse_stats_year_2024["placement"]["2"],
                            horse_stats_year_2024["placement"]["3"],
                            horse_stats_year_2024["winPercentage"]
                        ])

                # trainer stats
                trainerStats = horseTrainer['statistics']['years']
                if (trainerStats is not None):
                    if (trainerStats.get('2023') is not None):
                        horse_trainer_stats_2023 = trainerStats['2023']
                        features_vector.append([
                            horse_trainer_stats_2023["starts"],
                            horse_trainer_stats_2023["earnings"],
                            horse_trainer_stats_2023["placement"]["1"],
                            horse_trainer_stats_2023["placement"]["2"],
                            horse_trainer_stats_2023["placement"]["3"],
                            horse_trainer_stats_2023["winPercentage"]
                        ])

                    if (trainerStats.get('2024') is not None):
                        horse_trainer_stats_2024 = trainerStats['2024']

                        features_vector.append([
                            horse_trainer_stats_2024["starts"],
                            horse_trainer_stats_2024["earnings"],
                            horse_trainer_stats_2024["placement"]["1"],
                            horse_trainer_stats_2024["placement"]["2"],
                            horse_trainer_stats_2024["placement"]["3"],
                            horse_trainer_stats_2024["winPercentage"]
                        ])

                raceHorseResult = []

                raceHorseResult.append([
                    raceResult['place']
                ])

                features_vector.extend(raceHorseResult)

                feature_flatten = []
                for feature in features_vector:
                    feature_flatten.extend(feature)
                features.append(feature_flatten)

    return features, np.array(columns)


features, columns = race_data(load_data('../results.json'))
df = pd.DataFrame(features, columns=columns)
df = df.fillna(0)


X = df.drop(columns=['horse_placement']).values
dy = df['horse_placement'].values


y = []
for ys in dy:
    # print(ys)
    if isnan(ys):
        y.append(0)
    else:
        y.append(ys)

# print(y)


scalar = MinMaxScaler()

X = scalar.fit_transform(X)

# # Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
#
#
# # Convert to TensorFlow Dataset
train_dataset = tf.data.Dataset.from_tensor_slices(
    (X_train, y_train)).batch(32)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32)

# Define the model
model = kr.Sequential([
    kr.layers.Input(shape=(X_train.shape[1],)),
    kr.layers.Dense(64, activation='relu'),
    kr.layers.Dense(32, activation='relu'),
    kr.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error',
              metrics=['mean_absolute_error'])
# # Train the model
model.fit(train_dataset, epochs=10)
#
# # Evaluate the model
model.evaluate(test_dataset)
#
# # Save the model
model.save('horse_racing_model.h5')

# Load and preprocess new test data
new_data = load_data('results.json')  # Load new test data
test_features, test_columns = race_data(new_data)
test_df = pd.DataFrame(test_features, columns=test_columns)
test_df = test_df.fillna(0)

# Separate features (X_test_new)
X_test_new = test_df.drop(columns=['horse_placement']).values

# Normalize features
# Use the same scaler fitted on the training data
X_test_new = scalar.transform(X_test_new)

# Make predictions
predictions = model.predict(X_test_new)

# Actual placements (if available)
actual_placements = test_df['horse_placement'].values

# Print predictions with relevant details
actual_placements = test_df['horse_placement'].values
print("Placements:")
for i, pred in enumerate(predictions):
    actual = actual_placements[i] if i < len(actual_placements) else "Unknown"
    print(f"Horse {i+1}: Predicted placement = {pred[0]} Actual Placement = {actual}")



def mean_absolute_error(actual, predicted):
    mae:np.ndarray = kr.metrics.mean_absolute_error(actual, predicted)

    print(f"Mean Absolute Error: {np.mean(mae)}")
    print("Mean Absolute Error (MAE) Summary:")
    print(f"Mean: {np.mean(mae)}")
    print(f"Median: {np.median(mae)}")
    print(f"Standard Deviation: {np.std(mae)}")
    print(f"Min: {np.min(mae)}")
    print(f"Max: {np.max(mae)}")

    # Generate random predictions within the range of actual placements
    min_placement = np.min(actual)
    max_placement = np.max(actual)
    random_predictions = np.random.uniform(min_placement, max_placement, len(actual))

    # Calculate MAE for random predictions
    random_mae = np.mean(np.abs(random_predictions - actual))
    print(f"Random Predictor MAE: {random_mae}")

    # Compare with your model's MAE
    model_mae = np.mean(mae)
    print(f"Model MAE: {model_mae}")
    print(f"Improvement over Random: {random_mae - model_mae}")





    # Visualize Actual vs. Predicted Placements
    plt.scatter(actual, predicted, alpha=0.5)
    plt.plot([min_placement, max_placement], [min_placement, max_placement], 'r--')
    plt.title("Actual vs. Predicted Placements")
    plt.xlabel("Actual Placements")
    plt.ylabel("Predicted Placements")
    plt.show()
