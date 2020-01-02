'''
特征匹配和Homography查找对象：
1.将特征匹配和calib3d模块混合起来，找到复杂图像中的对象。
2.将来自calib3d模块的特征匹配和findHomography
3.可以使用cv2.findHomography()。如果找到这两个图像中的一组点，它将找到该对象的每个变换。
4.然后使用cv2.perspectTransform()来查找对象。它至少需要四个正确的点来找到转换。
5.匹配的时候可能会有一丢丢错误。
栗子：
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
import os
from util import *

MIN_MATCH_COUNT = 5
 
template_path = ".\\template"


 
def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir) 
    elif os.path.isdir(dir): 
        for s in os.listdir(dir): 
            newDir = os.path.join(dir,s)
            get_filelist(newDir, Filelist)
    return Filelist
 
 
def standing_cap_detection(imagePath):
    a = []
    filelist = get_filelist(template_path,a)
    print(filelist)
    reslist = []
    for file in filelist:
        template = cv2.imread(file,0) 
        (tH, tW) = template.shape[:2]
        print(file)

        image = cv2.imread(imagePath,0) 
        #image smaller make faster

        res = SIFT(template,image)
        print(res)
        if res is not None:
            reslist.append( res)

    return reslist

def SIFT(img1,img2):

    # 初始化SIFT探测器
    # sift = cv2.xfeatures2d.SIFT_create()
    
    # 初始化surf探测器
    
    sift = cv2.xfeatures2d.SURF_create()
    # 海塞矩阵阈值，在这里调整精度，值越大点越少，越精准 
    # 用SIFT找到关键点和描述符
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    
    good = []
    for m, n in matches:
        if m.distance < 0.7* n.distance:
            good.append(m)
    
    '''
    现在我们设置一个条件，即至少10个匹配（由MIN_MATCH_COUNT定义）将在那里以找到该对象。
    否则，只需显示一条消息，说明没有足够的匹配。
    如果找到足够的匹配，我们将提取两个图像中匹配关键点的位置。
    他们通过寻找这种转变。 一旦我们得到这个3x3转换矩阵，
    我们就用它来将queryImage的角点转换成trainImage中相应的点。 然后我们绘制它。
    '''
    res =None
    if len(good) > MIN_MATCH_COUNT:
        print(len(good))
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    
        # M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)
        M, mask = cv2.findHomography(src_pts, dst_pts,0,confidence = 1.0)
        matchesMask = mask.ravel().tolist()
    
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
    
        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        res = [np.int32(dst)] 
    
    else:
        print("Not enough matches are found", (len(good), MIN_MATCH_COUNT))
        matchesMask = None
    
    # 最后绘制内点(如果成功找到对象)或匹配关键点(如果失败)
    
    draw_params = dict(matchColor=(0, 255, 0),
                    singlePointColor=None,
                    matchesMask=matchesMask,
                    flags=2)
    
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
    # cv2.imshow("Window", img3) 
    # cv2.waitKey(0)
    return res