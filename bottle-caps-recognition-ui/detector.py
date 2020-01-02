from standing_cap_detection import *
from pro_con_cap_detection import *
from PIL import Image, ImageFilter, ImageGrab, ImageDraw, ImageFont


class Detector:

    def __init__(self):
        self.pro_con_detector = ProConDetector()

    def pro_con_detect(self, image_path, threshold):
        return self.pro_con_detector.detect(image_path, threshold)

    # 返回临时文件名
    def standing_cap_detect(self, image_path):
        location = standing_cap_detection(image_path)
        return self.sign_with_rect_and_text(image_path, location, "standing_cap")

    # location: the location to draw rect; text: signal text
    def sign_with_rect_and_text(self, image_path, location, text):
        im = Image.open(image_path)
        draw = ImageDraw.Draw(im)
        draw.rectangle(location, outline='blue', width=2)

        font = ImageFont.truetype("consola.ttf", 40, encoding="unic")  # 设置字
        draw.text(location, text, 'fuchsia', font)
        temp_filename = "temp.png"
        im.save(temp_filename)
        return temp_filename

