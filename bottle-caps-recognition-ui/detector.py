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

        for loc in locations:
            for cap in loc:
                print("cap")
                sum = 0
                xmean = 0
                ymean = 0
                for i in range(0,4):
                    sum=sum+1
                    x = cap[i][0][0]
                    y = cap[i][0][1]
                    xmean += x
                    ymean += y
                
                xmean = xmean//sum
                ymean = ymean//sum
                cv2.circle(img,(xmean,ymean),3,(0,0,213),-1)
                coordinate = "(" + str(xmean) + ", " + str(ymean) + ")"
                cv2.putText(img, coordinate, (xmean, ymean+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return img

