#! /usr/bin/env python
# coding: utf-8

import sys
import numpy as np
import cv2

# esc key (end)
ESC_KEY = 0x1d
# p key (pause)
P_KEY = 0x70
# s key (save data and restart)
S_KEY = 0x73
# intervel of receive key
INTERVAL = 1


class Motion:
    # constructor
    def __init__(self, inputFilePath):
        cv2.namedWindow("select feature point")
        cv2.setMouseCallback("select feature point", self.mouse_event)
        self.video = cv2.VideoCapture(inputFilePath)
        self.interval = INTERVAL
        self.frame = None
        self.features = None
        self.status = None
        self.frameNum = 0

    # main method
    def run(self):
        if not(self.video.isOpened()):
            print("Can not read movie file")
            sys.exit(1)

        # processing of initial frame
        ret, self.frame = self.video.read()

        while ret:
            self.features = None
            self.frameNum += 1
            # display image
            cv2.imshow("select feature point", self.frame)
            # processing of next frame
            ret, self.frame = self.video.read()

            # each key operation
            key = cv2.waitKey(self.interval)
            if key == ESC_KEY:
                break
            elif key == P_KEY:
                self.interval = 0
            elif key == S_KEY:
                self.save_data()
                self.interval = INTERVAL

        # end processing
        cv2.destroyAllWindows()
        self.video.release()


    # select feature point by mouse left click
    def mouse_event(self, event, x, y, flags, param):
        # other than left click
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        # draw and add feature point
        cv2.circle(self.frame, (x, y), 4, (0, 0, 255), -1, 8, 0)
        self.add_feature(x, y)
        cv2.imshow("select feature point", self.frame)
        return


    # add new feature point
    def add_feature(self, x, y):
        if self.features is None:
            self.features = np.array([[x, y]], np.uint16)
            self.status = np.array([1])
        else:
            self.features = np.append(self.features, [[x, y]], axis=0).astype(np.uint16)
            self.status = np.append(self.status, 1)

    # save cordinate and figure. there are feature point information
    def save_data(self):
        if self.features is None:
            print("Not select feature")
        else:
            cv2.imwrite("../image/{}.png".format(self.frameNum), self.frame)
            #convert: opencv axis -> matplotlib axis
            print(self.frame.shape[1])
            self.features[:, 1] = self.frame.shape[0] - self.features[:, 1]
            np.savetxt("../data/{}.csv".format(self.frameNum), self.features, delimiter=",", fmt="%d")
            print("save data frame number: {}".format(self.frameNum))
        return


if __name__ == "__main__":
    inputFilePath = input("input movie file path: ")
    Motion(inputFilePath).run()