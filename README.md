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

###### 优点

- 可应对旋转缩放、尺度缩放
- 速度相对较快

###### SURF 算法

基于高斯图像，计算每一个像素点的Hessian矩阵行列式，利用该行列式近似得到变换图像，用于找到特征点。

###### SURF和SIFT的区别

SURF是在SIFT的基础上改进而生，不仅提高了计算速度，而且更加安全鲁棒性。

SIFT需要计算高斯差分图像（DoG），用于find特征点。在sift中需要进行下采样操作。

###### 对于传统模板匹配算法的改进

传统模板匹配的缺陷在于不具有旋转不变形，若待匹配的图进行了旋转，那么这种滑窗的模板匹配方法当即失效。使用传统的模板匹配速度较快，但是无法应对旋转和缩放问题。要解决旋转不变的问题，必须要得到旋转不变的特征量，例如特征点。

使用SURF计算得到模板和待匹配图像的特征点，然后使用FLANN进行特征点匹配， 最后进行仿射变换便可得到匹配的位置。

###### FLANN算法

FLANN是高维数据的快速最近邻算法。

SIFT/SURF算法中需要做特征点匹配，特征点匹配实际上就是一个通过距离函数在高维矢量之间进行相似性检索的问题。针对如何快速而准确地找到查询点的近邻，现在提出了很多高维空间索引结构和近似查询的算法，k-d树就是其中一种。

在计算机视觉和机器学习中，对于一个高维特征，找到训练数据中的最近邻计算代价是昂贵的。

所以FLANN的搜索过程较为合适，采用 FLANN 的 KD-TREE 搜索相似的特征矢量，在不影响图像匹配速度的前提下， 可以提高特征匹配率准确率。[1]

###### 海量数据最近邻查找的 KD-TREE 

KD-TREE 是一种分割k维数据空间的数据结构（对数据点在k维空间中划分的一种数据结构），是一种高维索引树形数据结构。 KD-TREE 是二进制空间分割树的特殊的情况。 KD-TREE 是一种平衡二叉树。

效果：

![avatar](https://github.com/Dianaaaa/bottle-caps-recognition/blob/master/report_image/template_matching.PNG)
# 一些有用的资料

如何用python+opencv调用手机的摄像头：

 https://blog.csdn.net/baidu_33512336/article/details/86682806 



###### 参考资料

[1]基于SURF特征提取和FLANN搜索的图像匹配算法_冯亦东