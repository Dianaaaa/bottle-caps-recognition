import cv2

cv2.namedWindow("camera", 1)

# 开启ip摄像头
video = "http://admin:admin@10.162.175.247:8081"

cap = cv2.VideoCapture(video)

while True:
    ret, image_np = cap.read()

    # height = 600
    # width = 1000

    cv2.imshow('object detection', image_np)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
