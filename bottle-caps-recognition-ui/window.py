import sys
import os
import PyQt5
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QAction, QFileDialog, QSlider, QLCDNumber)
from PyQt5.QtGui import (QIcon, QImage, QPixmap)
import cv2
from detector import Detector


class Window(QMainWindow):

    # 获取目前的pic
    def get_cur_pic(self):
        return self.chosen_pics[self.cur_index].replace("/", "\\")

    # 设置窗口底部的status bar
    def show_status(self, status):
        self.statusBar().showMessage(status)

    # 传递filename来显示检测结果
    def show_result_filename(self, filename):
        self.output_label.setPixmap(QPixmap(filename))

    # 传递三维数组来显示结果
    def show_result_matrix(self, img):
        self.output_label.setPixmap(self.matrix2pixmap(img))

    def __init__(self, parent=None):
        super().__init__()
        self.detector = Detector()
        # self.height self.width
        # 定义部件
        self.menubar = None
        self.file_menu = None
        self.pic_action = None
        self.pic_label = None
        self.output_label = None
        self.prev_button = None
        self.next_button = None
        self.detect_button = None
        self.slider = None
        # 图片显示
        self.chosen_pics = ["image.png"]
        self.cur_index = 0
        # 初始化
        self.init_ui()

    def init_ui(self):
        # 设置标题和窗口大小
        self.setGeometry(100, 100, 1280, 720)  # 前两个参数是显示窗口的位置
        self.setWindowTitle("瓶盖识别")
        # debug slider
        # self.slider = QSlider(Qt.Horizontal, self)
        # self.slider.move(100, 660)
        # lcd = QLCDNumber(self)
        # lcd.move(300, 660)
        # self.slider.setMaximum(255)
        # self.slider.valueChanged.connect(lcd.display)
        # 初始化部件
        self.menubar = self.menuBar()  # 菜单栏
        self.pic_action = QAction(QIcon("image.png"), "图片", self)  # 菜单栏选择图片action
        self.pic_action.setStatusTip("选择图片")
        self.file_menu = self.menubar.addMenu("文件")  # 菜单栏菜单
        self.file_menu.addAction(self.pic_action)
        self.pic_label = QLabel(self)  # 图片显示label
        self.pic_label.setGeometry(QRect(50, 50, 480, 600))
        self.pic_label.setScaledContents(True)
        self.output_label = QLabel(self)
        self.output_label.setGeometry(QRect(690, 50, 480, 600))
        self.output_label.setScaledContents(True)
        self.prev_button = QPushButton("上一张", self)  # 上一张按钮
        self.next_button = QPushButton("下一张", self)  # 下一站按钮
        self.detect_button = QPushButton("识别", self)  # 识别按钮
        self.prev_button.move(850, 660)
        self.detect_button.move(1000, 660)
        self.next_button.move(1150, 660)
        # 部件事件连接
        self.pic_action.triggered.connect(self.open_pic)
        self.prev_button.clicked.connect(self.click_prev)
        self.detect_button.clicked.connect(self.click_detect)
        self.next_button.clicked.connect(self.click_next)
        self.set_button_enabled()
        # 显示窗口
        self.show()

    def open_pic(self):
        pics = QFileDialog.getOpenFileNames(self, "选择图片", "./")
        if len(pics[0]) > 0:
            self.chosen_pics = pics[0]
            self.show_pic()
            self.set_button_enabled()
        else:
            self.show_status("no picture chosen")

    def get_pic(self, i):
        return self.chosen_pics[i].replace("/", "\\")

    @staticmethod
    def matrix2pixmap(matrix):
        height, width, bytesPerComponent = matrix.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB, matrix)
        qimg = QImage(matrix.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def show_pic(self):
        self.clean_output()
        img = cv2.imread(os.path.abspath(self.get_pic(self.cur_index)))
        self.pic_label.setPixmap(self.matrix2pixmap(img))

    def click_prev(self):
        self.cur_index = self.cur_index - 1
        self.show_pic()
        self.set_button_enabled()

    def click_next(self):
        self.cur_index = self.cur_index + 1
        self.show_pic()
        self.set_button_enabled()

    def click_detect(self):
        image_path = self.get_pic(self.cur_index)
        # self.show_result_filename(self.detector.standing_cap_detect(image_path))
        # cv2.imshow("Image", self.detector.pro_con_detect(image_path, self.slider.value()))
        self.show_result_matrix(self.detector.all_detect(image_path))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def clean_output(self):
        self.output_label.setPixmap(QPixmap(""))

    def set_button_enabled(self):
        pic_amount = len(self.chosen_pics)
        if pic_amount == 0:
            self.detect_button.setEnabled(False)
        else:
            self.detect_button.setEnabled(True)
        if self.cur_index == 0:
            self.prev_button.setEnabled(False)
        else:
            self.prev_button.setEnabled(True)
        if self.cur_index == pic_amount-1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)



