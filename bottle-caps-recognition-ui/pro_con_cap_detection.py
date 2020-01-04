import argparse
import imutils
import cv2
import numpy as np
from predict import *


class ProConDetector:

    def __init__(self):
        pass

    def detect(self, image_path, threshold):
        image = cv2.imread(image_path)
        # return self.hough_detect(image, threshold)
        return self.contour_detect(image, threshold)

    # 会莫名没检测到一些圆
    def hough_detect(self, origin_image, threshold):
        # convert the image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(origin_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = 255 - thresh
        # use canny to detect boundary
        canny = cv2.Canny(thresh, 50, 150)
        # use hough to detect circles
        circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=10, maxRadius=400)
        # print(circles)
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(origin_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(origin_image, (i[0], i[1]), 2, (0, 0, 255), 3)
        return origin_image

    def contour_detect(self, origin_image, threshold):
        # load the image and resize it to a smaller factor so that
        # the shapes can be approximated better
        resized = imutils.resize(origin_image, width=300)
        ratio = origin_image.shape[0] / float(resized.shape[0])
        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = 255 - thresh
        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        rects = []
        for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            else:
                continue
            shape = self.contour2shape(c)
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then get the rect
            if shape == "circle":
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                x, y, w, h = cv2.boundingRect(c)
                rects.append((x, y, w, h, cX, cY))

        rects = self.remove_overlap(rects)

        for rect in rects:
            x, y, w, h, cX, cY = rect
            crop = origin_image[y-10:y+h+10, x-10:x+w+10]
            grayImg = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            pro_con = predict(grayImg)
            # pro_con = 1
            cv2.rectangle(origin_image, (x-10, y-10), (x+w+10, y+h+10), (0, 255, 0), 2)
            # cv2.putText(origin_image, "circle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            temp_text = ""
            if pro_con == 0:
                temp_text = "back"
            if pro_con == 1:
                temp_text = "front"
            cv2.putText(origin_image, temp_text, (cX, cY+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            coordinate = "(" + str(cX) + ", " + str(cY) + ")"
            cv2.putText(origin_image, coordinate, (cX, cY+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # cv2.drawContours(origin_image, [c], -1, (0, 255, 0), 2)
        return origin_image

    def contour2shape(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        if peri < 100:
            return shape
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape

    @staticmethod
    def remove_overlap(rects):
        noverlap_rects = []
        for i in range(len(rects)):
            x, y, w, h, cX, cY = rects[i]
            flag = True
            for j in range(len(rects)):
                if i == j:
                    continue
                x1, y1, w1, h1, cX1, cY1 = rects[j]
                if x > x1 and y > y1 and x + w < x1 + w1 and y + h < y1 + h1:
                    flag = False
                    break
            if flag:
                noverlap_rects.append(rects[i])
        return noverlap_rects

