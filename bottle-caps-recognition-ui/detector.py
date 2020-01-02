from standing_cap_detection import *
from pro_con_cap_detection import *
from PIL import Image, ImageFilter, ImageGrab, ImageDraw, ImageFont


class Detector:

    def __init__(self):
        self.pro_con_detector = ProConDetector()

    def all_detect(self, image_path):
        img = self.pro_con_detect(image_path, 120)
        locations = self.standing_cap_detect(image_path)
        return self.sign_with_rect_and_text(img, locations, "standing")

    def pro_con_detect(self, image_path, threshold):
        return self.pro_con_detector.detect(image_path, threshold)

    # 返回临时文件名
    @staticmethod
    def standing_cap_detect(image_path):
        return standing_cap_detection(image_path)

    # location: the location to draw rect; text: signal text
    @staticmethod
    def sign_with_rect_and_text(img, locations, text):
        for location in locations:
            cv2.polylines(img, location, True, 255, 3, cv2.LINE_AA)
        return img

