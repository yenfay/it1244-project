# 1D-CNN with classification + regression heads
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import (
    Conv1D,
    MaxPooling1D,
    GlobalAveragePooling1D,
    Dense
)
from tensorflow.keras.optimizers import Adam

def build_cnn(input_shape=(1000, 16), # every 10 seconds, 16 sensors
              task="regression",
              learning_rate=0.001):

    # Create the CNN architecture.
    # Input: 1000 time steps and 16 gait sensor channels.
    model = Sequential([
        Input(shape=input_shape),
        Conv1D(32, 3, activation="relu", padding="same"), # Extract local temporal patterns.
        MaxPooling1D(2), # Reduce the temporal dimension.
        Conv1D(64, 3, activation="relu", padding="same"), # Extract higher-level temporal patterns
        GlobalAveragePooling1D(), # Summarise the 64 learned feature maps.
        Dense(32, activation="relu") # Combine extracted features before prediction.
    ])

    # for function to support regression and classification 
    if task == "classification": # for task 1
        model.add(Dense(1, activation="sigmoid")) # sigmoid converts output to probability
        loss = "binary_crossentropy"
        metrics = ["accuracy"] # note: should use other performance metrics in later evaluation 
        
    elif task == "regression": # for task 2
            model.add(Dense(1)) # linear for output continuous prediction 
            loss = "mse"
            metrics = ["mae"]

    else:
        raise ValueError("Task must be 'classification' or 'regression'.")

    # Configure the model for training.
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss=loss,
        metrics=metrics
    )

    return model