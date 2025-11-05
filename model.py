from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO("yolov8n.pt")


# Perform object detection on an image
results = model.predict(source='test.png', conf=0.2, iou=0.7, classes=[0], save=False)
print(results[0])
boxes = results[0].boxes#.xyxy.cpu().numpy()
img = cv2.imread('test.png')

for i, box in enumerate(boxes):
    conf = box.conf[0]
    text = f'Person {round(conf.item(), 2)}'
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    #text_y = max(y1 - 10 - (i * 15), 15)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)  # Зеленый прямоугольник


    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
    print(text_w)
    text_x = x1
    text_y = y1 - 10
    if text_y < 15:
        text_y = y1 + text_h + 5 

    cv2.putText(img, text, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)


cv2.imshow('Image', img)
cv2.waitKey(0)