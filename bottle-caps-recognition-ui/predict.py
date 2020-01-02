import joblib
import cv2
import numpy as np
import os


sift=cv2.xfeatures2d.SIFT_create()
knn = joblib.load('./knn_model.m')
svm = joblib.load('./svm_model.m')

def predict(img):
    # pre-process
    gray= img
    gray=cv2.resize(gray, (400, 400), interpolation=cv2.INTER_AREA)
    gray=cv2.equalizeHist(gray)
    keypoints, des=sift.detectAndCompute(gray, None)

    # predict
    img_clustered_word = knn.predict(des)
    img_bow_hist = np.array(np.bincount(img_clustered_word, minlength=252))
    X = img_bow_hist

    pred = svm.predict([X])
    return pred



if __name__ == '__main__':
    filepath = './Test/pros/'
    filelist = os.listdir(filepath)
    for filename in filelist:
        print(filename)
        if filename == ".gitkeep":
            continue
        # print(os.path.join(filepath, filename))
        img=cv2.imread(os.path.join(filepath, filename),0)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
        result = predict(img)
        if result == 0:
            print("fan")
        if result == 1:
            print("zheng")