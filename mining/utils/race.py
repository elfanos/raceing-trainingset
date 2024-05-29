
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import keras as kr
from math import isnan

# Load data from JSON file
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Adding horse identifiers and historical features
def add_historical_features(data, num_previous_races=5):
    horse_history = {}
    for horseData in data:
        for race in horseData['races']:
            for raceStart in race['starts']:
                horse_id = raceStart['horse']['id']
                if horse_id not in horse_history:
                    horse_history[horse_id] = {'placements': [], 'times': []}
                # Add historical features
                if len(horse_history[horse_id]['placements']) >= num_previous_races:
                    raceStart['historical_avg_placement'] = np.mean(horse_history[horse_id]['placements'][-num_previous_races:])
                    raceStart['historical_avg_time'] = np.mean(horse_history[horse_id]['times'][-num_previous_races:])
                else:
                    raceStart['historical_avg_placement'] = np.mean(horse_history[horse_id]['placements'])
                    raceStart['historical_avg_time'] = np.mean(horse_history[horse_id]['times'])

                # Update history
                horse_history[horse_id]['placements'].append(raceStart['result']['place'])
                horse_history[horse_id]['times'].append(raceStart['horse']['record']['time']['minutes'])

def race_data(data):
    features = []
    columns = ['start_number', 'start_postPosition', 'horse_record_minutes', 'horse_placement',
               'horse_record_seconds', 'horse_record_tenths', 
               'historical_avg_placement', 'historical_avg_time']
    # Additional column setup ...

    for horseData in data:
        for race in horseData['races']:
            for raceStart in race['starts']:
                features_vector = []
                horseStart = raceStart['horse']
                record = horseStart['record']
                recordTime = record['time']
                raceResult = raceStart['result']

                start = [raceStart['number'], raceStart['postPosition']]
                result = [raceResult['place']]
                horse = [recordTime['minutes'], recordTime['seconds'], recordTime['tenths']]
                historical_features = [raceStart['historical_avg_placement'], raceStart['historical_avg_time']]

                features_vector.extend(start)
                features_vector.extend(result)
                features_vector.extend(horse)
                features_vector.extend(historical_features)

                features.append(features_vector)

    return features, np.array(columns)

# Load and preprocess data
data = load_data('../results.json')
add_historical_features(data)
features, columns = race_data(data)
df = pd.DataFrame(features, columns=columns)
df = df.fillna(0)

X = df.drop(columns=['horse_placement']).values
y = df['horse_placement'].values

scalar = MinMaxScaler()
X = scalar.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to TensorFlow Dataset
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(32)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32)

# Define the model with Dense layers
model = kr.Sequential([
    kr.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    kr.layers.Dense(32, activation='relu'),
    kr.layers.Dense(1, activation='linear')  # Use linear activation for regression
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Train the model
model.fit(train_dataset, epochs=10)

# Evaluate the model
model.evaluate(test_dataset)

# Save the model
model.save('horse_racing_model.h5')

# Load the saved model
model = kr.models.load_model('horse_racing_model.h5')

# Load and preprocess new test data
new_data = load_data('results.json')
add_historical_features(new_data)
test_features, test_columns = race_data(new_data)
test_df = pd.DataFrame(test_features, columns=test_columns)
test_df = test_df.fillna(0)

# Separate features (X_test_new)
X_test_new = test_df.drop(columns=['horse_placement']).values

# Normalize features
X_test_new = scalar.transform(X_test_new)

# Make predictions
predictions = model.predict(X_test_new)

# Print predictions with relevant details
print("Predicted Placements:")
actual_placements = test_df['horse_placement'].values
for i, pred in enumerate(predictions):
    print(f"Horse {i+1}: Predicted Placement = {pred[0]}, actual placement = {actual_placements[i]}")

# Calculate Mean Absolute Error for the new data
new_mae = kr.metrics.mean_absolute_error(actual_placements, predictions)
print(f"\nMean Absolute Error on new data: {new_mae.numpy()}")
