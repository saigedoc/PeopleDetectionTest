import cv2
from ultralytics import YOLO

def video_process(pathin, pathout, model_path, progress_bar=None):
    video = cv2.VideoCapture(pathin)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    video_out = cv2.VideoWriter(pathout, fourcc, fps, (width, height))
    try:
        model = YOLO(model_path)
    except:
        raise Exception("Error. Ошибка загрузки весов, убедитесь, что выбрали правильный файл.")
    if not video.isOpened():
        raise Exception("Error. Ошибка открытия видео, убедитесь что вы выбрали правильный файл.")
    frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(frames_count):
        if progress_bar:
            progress_bar.setValue(int(i / frames_count * 100))
        ret, frame = video.read()
        if not ret:
            raise Exception("Error. Ошибка чтения видео, убедитесь что вы выбрали правильный файл.")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_frame = model.predict(source=rgb_frame, conf=0.2, iou=0.7, classes=[0], save=False, verbose=False)

        boxes = detected_frame[0].boxes

        for box in boxes:
            conf = box.conf[0]
            text = f'Person {round(conf.item(), 2)}'
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(rgb_frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        video_out.write(frame)
    video.release()
    video_out.release()

if __name__ == "__main__":
    video_process("crowd.mp4", "new.mp4")