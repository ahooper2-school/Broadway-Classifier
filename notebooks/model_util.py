# util for loading a model for transfer learning
import keras
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.models import Sequential, Model

HEIGHT = 128
WIDTH = 128
NUM_CLASSES = 41
FC_LAYERS = [1024, 1024]
DROPOUT = 0.5
NUM_EPOCHS = 10
BATCH_SIZE = 32

def build_finetune_model(base_model, dropout, fc_layers, num_classes, trainable=False):
    for layer in base_model.layers:
        layer.trainable = trainable

    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        # New FC layer, random init
        x = Dense(fc, activation='relu')(x) 
        x = Dropout(dropout)(x)

    # New softmax layer
    predictions = Dense(num_classes, activation='softmax')(x) 
    
    finetune_model = Model(inputs=base_model.input, outputs=predictions)

    return finetune_model

def remove_top_layer(base_model, num_classes):
    # remove the top layer so we can add dense layer with correct number of classes
    predictions = Dense(num_classes, activation='softmax')(base_model.layers[-2].output)
    model = Model(inputs=base_model.input, outputs=predictions)
    return model
