# Further processing for TensorFlow (if required)
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import keras as kr 
from statistic import statistic_df


data = {
    "2023": {
        "starts": 375,
        "earnings": 338424900,
        "placement": {
            "1": 49,
            "2": 40,
            "3": 32
        },
        "winPercentage": 1306
    },
    "2024": {
        "starts": 126,
        "earnings": 138823300,
        "placement": {
            "1": 29,
            "2": 15,
            "3": 9
        },
        "winPercentage": 2301
    }
}

df = statistic_df(data)
print(df)

scaler = MinMaxScaler()
X = scaler.fit_transform(df.drop(columns=["winPercentage"]))
y = df["winPercentage"].values
#
#
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(buffer_size=len(X)).batch(2)
#
#
model = kr.Sequential([
    kr.layers.Input(shape=(X.shape[1],)),
    kr.layers.Dense(64, activation='relu' ),
    kr.layers.Dense(32, activation='relu'),
    kr.layers.Dense(1)
])
#
model.compile(optimizer='adam', loss='mean_squared_error')

model.summary()



