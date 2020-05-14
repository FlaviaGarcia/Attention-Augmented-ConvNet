# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:14:49 2020

@author: matte
"""

import sys
sys.path.append("..")

import tensorflow.keras
from models.resnet50 import resnet50_v1
from models.augmented_resnet import resnet50_att_augmented_v1
from cifar10_dataset.data_loader import get_train_val_test_datasets
import numpy as np
from preprocessing.augmentation import Augment2D
from engine.learning_rate.linear_cos_annealing import LinearCosAnnelingLrSchedule
from engine.training.custom_training import TrainingEngine
from engine.learning_rate.step import StepLearningRate
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

validation_size = 5000
batch_size = 128 
epochs = 220

if __name__ == "__main__":
        
    x_train, y_train, x_val, y_val, x_test, y_test = get_train_val_test_datasets(validation_size)
    
    print("Data loaded.")
    
    train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    validation_data = tf.data.Dataset.from_tensor_slices((x_val, y_val))
    test_data = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    
    input_shape = x_train.shape[1:]
    n_colors = x_train.shape[3]
    depth = n_colors * 6 + 2
    k = 0.2
    v = 0.1
    model = resnet50_att_augmented_v1(input_shape, depth, v, k, n_heads=8)


    training_module = TrainingEngine(model)
    training_module.lr_scheduler = StepLearningRate()
    training_module.optimizer = Adam(lr=training_module.lr_scheduler.get_learning_rate(0))
    training_module.fit(train_data,
                          validation_data,
                          batch_size=batch_size,
                          epochs=epochs,
                          data_augmentation=False)

    
    scores = training_module.evaluate(test_data)
    print('Test loss:', scores[1])
    print('Test accuracy:', scores[0])