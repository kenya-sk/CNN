#! /usr/bin/env python
#coding: utf-8

import numpy as np
import pandas as pd
import csv
from scipy import optimize

from clustering import clustering
from cnn_pixel import get_masked_index


def get_ground_truth(ground_truth_path, mask_path=None):
    """
    plots the coordinates of answer label on the black image(all value 0) and
    creates a correct image for accuracy evaluation.

    input:
        ground_truth_path: coordinates of the estimated target (.csv)
        mask_path: enter path only when using mask image

    output:
        array showing the positon of target
    """

    ground_truth_arr = np.array(pd.read_csv(ground_truth_path))
    if mask_path is None:
        return ground_truth_arr
    else:
        valid_h, valid_w = get_masked_index(mask_path)
        valid_ground_truth_lst = []

        for i in range(ground_truth_arr.shape[0]):
            index_w = np.where(valid_w == ground_truth_arr[i][0])
            index_h = np.where(valid_h == ground_truth_arr[i][1])
            intersect = np.intersect1d(index_w, index_h)
            if len(intersect) == 1:
                valid_ground_truth_lst.append([valid_w[intersect[0]], valid_h[intersect[0]]])
            else:
                pass
        return np.array(valid_ground_truth_lst)


def accuracy(est_centroid_arr, ground_truth_arr, dist_treshold):
    """
    the distance between the estimation and groundtruth is less than distThreshold --> True

    input:
        est_centroid_arr: coordinates of the estimated target (.npy). array shape == original image shape
        ground_truth_arr: coordinates of the answer label (.csv)
        dist_treshold: it is set maximum value of kernel width

    output:
        accuracy per frame
    """

    # make distance matrix
    n = max(len(est_centroid_arr), len(ground_truth_arr))
    dist_matrix = np.zeros((n,n))
    for i in range(len(est_centroid_arr)):
        for j in range(len(ground_truth_arr)):
            dist_cord = est_centroid_arr[i] - ground_truth_arr[j]
            dist_matrix[i][j] = np.linalg.norm(dist_cord)

    # calculate by hangarian algorithm
    row, col = optimize.linear_sum_assignment(dist_matrix)
    indexes = []
    for i in range(n):
        indexes.append([row[i], col[i]])
    valid_index_length = min(len(est_centroid_arr), len(ground_truth_arr))
    valid_lst = [i for i in range(valid_index_length)]
    if len(est_centroid_arr) >= len(ground_truth_arr):
        match_indexes = list(filter((lambda index : index[1] in valid_lst), indexes))
    else:
        match_indexes = list(filter((lambda index : index[0] in valid_lst), indexes))

    true_count = 0
    for i in range(len(match_indexes)):
        pred_index = match_indexes[i][0]
        truth_index = match_indexes[i][1]
        if dist_matrix[pred_index][truth_index] <= dist_treshold:
            true_count += 1

    accuracy = true_count / n
    print("******************************************")
    print("Accuracy: {}".format(accuracy))
    print("******************************************\n")

    return accuracy


if __name__ == "__main__":
    band_width = 25
    skip_lst = [15]
    for skip in skip_lst:
        accuracy_lst = []
        for file_num in range(1, 36):
            pred_dens_map = np.load("/data/sakka/estimation/test_image/model_201806142123/dens/{0}/{1}.npy".format(skip, file_num))
            centroid_arr = clustering(pred_dens_map, band_width, thresh=0.4)
            np.save("/data/sakka/estimation/test_image/model_201806142123/cord/{0}/{1}.npy".format(skip, file_num), centroid_arr)
            if centroid_arr.shape[0] == 0:
                print("Not found point of centroid\nAccuracy is 0.0")
                accuracy_lst.append(0.0)
            else:
                ground_truth_arr = get_ground_truth("/data/sakka/cord/test_image/{0}.csv".format(file_num), mask_path="/data/sakka/image/mask.png")
                accuracy_lst.append(accuracy(centroid_arr, ground_truth_arr, band_width))

        print("\n******************************************")
        print("Toal Accuracy (data size {0}, sikp size {1}): {2}".format(len(accuracy_lst), skip, sum(accuracy_lst)/len(accuracy_lst)))
        print("******************************************")

        with open("/data/sakka/estimation/test_image/model_201806142123/accuracy/{}/accuracy.csv".format(skip), "w") as f:
            writer = csv.writer(f)
            writer.writerow(accuracy_lst)
        print("SAVE: accuracy data")
