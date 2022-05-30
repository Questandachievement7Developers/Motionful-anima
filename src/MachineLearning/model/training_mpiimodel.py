#!/bin/python3
#creating model

#preconfigured library
import imp
import logging, os, sys, time, threading
from xml.etree.ElementInclude import include
import numpy as np
import tensorflow as tf
print(tf.__version__) #check the tensorflow version
#import tensorflow.contrib.slim as tfslim 
import tf_slim as tfslim

#customLibrary
# this is library for config file
from toolsetLib.configUtils import conf_load
from toolsetLib.datasetTool_factory import createDataset as create_dataset
from toolsetLib.loggingUtils import init_logger
# this is library for preloading data
from toolsetLib.nnet_toolset_posenet import getBatchSpecs as get_batch_spec
from toolsetLib.nnet_toolset_Factory import pose_net

class learningRate(obj):
    def __init__(own, config): 
        own.steps = config.multi_step
        own.current_step = 0
    def get_lr(own, iteration):
        lr = own.steps[own.current_step][0]
        if iteration == own.steps[own.current_step][1]:
            own.current_step += 1
        return lr

def preloadSetup(BatchesSpecs):
    # a placeholder for temporary data
    temp = {name: tf.placeholder(tf.float32, shape=spec) for (name, spec) in BatchesSpecs.items()}
    name = temp.keys()
    temp_list = list(temp.values())
    # a queue for temporary data
    QUEUE_VOLUME = 20
    queues = tf.FIFOQueue(QUEUE_VOLUME, [tf.float32]*len(BatchesSpecs))
    enqueue_op = queues.enqueue(temp_list)
    # a list for temporary data batches on the queue
    batches_list = queues.dequeue()

    batches = {}
    for idx, name in enumerate(name):
        batches[name] = batches_list[idx]
        batches[name].set_shape(BatchesSpecs[name])
    return batches, enqueue_op, temp

def loadnEnqueue(sessions, enqueue_op, coordinate, datasetFeed, temp):
    # load data and enqueue
    
    while not coordinate.should_stop():
        batch_np = datasetFeed.next_batch()
        food = {temp[name]: batch_np[name] for (name, temp) in temp.items()}
        sessions.run(enqueue_op, feed_dict=food)

def preloadStart(sessions, enqueue_op, datasetFeed, temp):
    # start preloading
    coordinate = tf.train.Coordinator()
    tensorThread = threading.Thread(target=loadnEnqueue, args=(sessions, enqueue_op, coordinate, datasetFeed, temp))
    # start thread
    tensorThread.start()
    return coordinate, tensorThread

def getOptimizer(lossOP, config):
    RateofLearning = tf.placeholder(tf.float32, shape=[])
    # get optimizer
    if config.optimizer == 'adam':
        optimizer = tf.train.AdamOptimizer(config.learning_rate)
    elif config.optimizer == "sgd":
        optimizer = tf.train.GradientDescentOptimizer(config.learning_rate)
    else:
        raise ValueError("Optimizer must be 'adam' or 'sgd'")
    train_op = optimizer.minimize(lossOP)
    return RateofLearning, train_op

def train():
    #Initiate Logger
    init_logger()
    #load config file
    config = conf_load() #to change the name of config file, change inside the function on the configUtils module
    datasetFeed = create_dataset(config)
    #determine the batch size
    batchSpec = get_batch_spec(config)
    batches, enqueue_op, temp = preloadSetup(batchSpec)
    #determine Loss function
    losses = pose_net(batches, config)
    total_loss = losses['total_loss']
    #merge loss
    for k, t in losses.items():
        tf.summary.scalar(k, t)
    mergedSum = tf.summary.merge_all()
    #state saver for saving model just like when you playing game and save state before playing on the boss stage
    savedVars = tfslim.get_variables_to_restore(include=["resnet_v1"])
    saveStateLoaderEngine = tf.train.Saver(savedVars)
    saveStateEngine = tf.train.Saver(max_to_keep=6) #maximum number of states to be saved

    #start the session after the states are managed
    sessionMain = tf.Session()
    #preloadCaching started
    coordinate, tensorThread = preloadStart(sessionMain, enqueue_op, datasetFeed, temp)
    #write summary to a file log
    summary_writer = tf.summary.FileWriter(config.log_dir, sessionMain.graph)
    #setLearningRate
    RateofLearning, train_op = getOptimizer(total_loss, config)
    #start the init session the session
    sessionMain.run(tf.global_variables_initializer())
    #start the required variable for the init session
    sessionMain.run(tf.local_variables_initializer())
    #load the state of the previous state using the determined engine
    saveStateLoaderEngine.restore(sessionMain, config.init_weights)
    maxIteration = int(config.multi_step[-1][1])
    displayCurrentIteration = config.display_iters
    #initialize cumulative loss variable
    cumulative_loss = 0.0
    learningRate_gen = learningRate(config)
    #start the training
    for iteration in range(maxIteration+1):
        #get the learning rate
        learningRate_value = learningRate_gen.get_lr(iteration)
        [_, loss_value, summary] = sessionMain.run([enqueue_op, total_loss, mergedSum], feed_dict={RateofLearning: learningRate_value})
        cumulative_loss += loss_value
        summary_writer.add_summary(summary, iteration)

        #display the loss
        if iteration % displayCurrentIteration == 0:
            #print("iteration: %d, loss: %f" % (iteration, cumulative_loss/displayCurrentIteration))
            logging.info("iteration: %d, loss: %f" % (iteration, cumulative_loss/displayCurrentIteration))
            cumulative_loss = 0.0
            
        #save state snapshot
        if (iteration % config.save_iters == 0) or (iteration == maxIteration):
            saveStateEngine.save(sessionMain, config.snapshot_prefix, global_step=iteration)

    #stop the session or kill session
    # stop the tensorThread
    sessionMain.close()
    coordinate.request_stop()
    coordinate.join([thread])


#start train function or method as a main thread
if __name__ == '__main__':
    train()

    