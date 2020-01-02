# bottle-caps-recognition
Detect bottle caps using pattern recognition

# 如何分析瓶盖正反

- 小样本的机器学习方法：

  - SIFT特征 + SVM支持向量机

  - 遇到的问题：经过SIFT算法，每张图产生的特征点数目不一样，得到的是关于特征点的信息的集合，不能直接输入到SVM中

  - 解决方法：SIFT + BOW。使用k-means将SIFT的所有特征点聚类，得到K个特征簇（词袋）。重新处理图片的sift特征向量：

    ```
    img_bow_hist = np.array(
            [np.bincount(clustered_words, minlength=n_clusters) for clustered_words in img_clustered_words])
    ```

    

    即数图片在每个特征簇下的特征点个数，得到等长的向量（K维），最后再输入到SVM中进行训练。

- 预测：

  将要预测的图片先预处理，然后使用SIFT+BOW模型得到描述图片特征的K维向量后，使用上一步训练的SVM模型进行预测。

# 如何检测立着的瓶盖

基于 SURF 特征提 取和快速近似近邻查找(fast library for approximate nearest neighbors, FLANN)搜索的图像 匹配算法。

优点：

- 可应对旋转缩放、尺度缩放
- 速度相对较快

传统模板匹配的缺陷在于不具有旋转不变形，若待匹配的图进行了旋转，那么这种滑窗的模板匹配方法当即失效。使用传统的模板匹配速度较快，但是无法应对旋转和缩放问题。要解决旋转不变的 问题，必须要得到旋转不变的特征量，例如特征点。

使用SURF计算得到模板和待匹配图像的特征点，然后使用FLANN进行特征点匹配， 最后进行仿射变换便可得到匹配的位置。

FLANN是高维数据的快速最近邻算法。

在计算机视觉和机器学习中，对于一个高维特征，找到训练数据中的最近邻计算代价是昂贵的。

所以FLANN的搜索过程较为合适，采用 FLANN 的 KD-TREE 搜索相似 的特征矢量，在不影响图像匹配速度的前提下， 可以提高特征匹配率准确率。[1]

效果：

https://github.com/Dianaaaa/bottle-caps-recognition/report_image/template_matching.PNG

# 一些有用的资料

如何用python+opencv调用手机的摄像头：

 https://blog.csdn.net/baidu_33512336/article/details/86682806 



###### 参考资料

[1]基于SURF特征提取和FLANN搜索的图像匹配算法_冯亦东