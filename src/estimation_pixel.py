#! /usr/bin/env python
# coding: utf-8

import math
import numpy as np
import tensorflow as tf
import cv2

import cnn_pixel


def main():
    X = tf.placeholder(tf.float32, [None, 72, 72, 3])
    y_ = tf.placeholder(tf.float32, [None])

    #model
    #layer1
    W_conv1 = tf.get_variable("conv1/weight1/weight1", [7,7,3,32])
    b_conv1 = tf.get_variable("conv1/bias1/bias1", [32])
    h_conv1 = tf.nn.relu(cnn_pixel.conv2d(X, W_conv1) + b_conv1)
    h_pool1 = cnn_pixel.max_pool_2x2(h_conv1)
    #layer2
    W_conv2 = tf.get_variable("conv2/weight2/weight2", [7,7,32,32])
    b_conv2 = tf.get_variable("conv2/bias2/bias2", [32])
    h_conv2 = tf.nn.relu(cnn_pixel.conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = cnn_pixel.max_pool_2x2(h_conv2)
    #layer3
    W_conv3 = tf.get_variable("conv3/weight3/weight3", [5,5,32,64])
    b_conv3 = tf.get_variable("conv3/bias3/bias3", [64])
    h_conv3 = tf.nn.relu(cnn_pixel.conv2d(h_pool2, W_conv3) + b_conv3)
    #layer4
    W_fc4 = tf.get_variable("fc4/weight4/weight4", [18*18*64, 1000])
    b_fc4 = tf.get_variable("fc4/bias4/bias4", [1000])
    h_conv3_flat = tf.reshape(h_conv3, [-1, 18*18*64])
    h_fc4 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc4) + b_fc4)
    #layer5
    W_fc5 = tf.get_variable("fc5/weight5/weight5", [1000, 400])
    b_fc5 = tf.get_variable("fc5/bias5/bias5", [400])
    h_fc5 = tf.nn.relu(tf.matmul(h_fc4, W_fc5) + b_fc5)
    #layer6
    W_fc6 = tf.get_variable("fc6/weight6/weight6", [400, 324])
    b_fc6 = tf.get_variable("fc6/bias6/bias6", [324])
    h_fc6 = tf.nn.relu(tf.matmul(h_fc5, W_fc6) + b_fc6)
    #layer7
    W_fc7 = tf.get_variable("fc7/weight7/weight7", [324, 1])
    b_fc7 = tf.get_variable("fc7/bias7/bias7", [1])
    h_fc7 = tf.nn.relu(tf.matmul(h_fc6, W_fc7) + b_fc7)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, "./model_pixel/model.ckpt")

        img = cv2.imread("../image/original/11_20880.png")
        dens = np.load("../data/dens/20/11_20880.npy")
        local_df = cnn_pixel.get_local_data(img, dens, 72)
        img_local = np.array(local_df["img_arr"])

        print("start estimation")
        estImg = []
        batchSize = 200
        n_batches = int(len(img_local) / batchSize)
        for batch in range(n_baches):
            print("batch: {0}/{1}".format(batch, n_baches))
            startIndex = batch * batchSize
            endIndex = startIndex + batchSize
            estImg.append(sess.run(h_fc7, feed_dict={X: np.vstack(img_local[startIndex:endIndex]).reshape(-1, 72, 72, 3)}))

        estImg = np.array(estImg).reshape(470, 720)
        np.save("./estimation.npy", estImg)
        print("save estimation data")


if __name__ == "__main__":
    main()