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



# 一些有用的资料

如何用python+opencv调用手机的摄像头：

 https://blog.csdn.net/baidu_33512336/article/details/86682806 