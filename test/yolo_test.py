from ultralytics import YOLO

model = YOLO('./result/yolov8_final_project/weights/best.pt')
model.predict(
    source='./test/theft.mp4',
    save=True,
    conf=0.25,
    project='./test/runs/detect',
    name='detect_result',
    save_txt=True
)
