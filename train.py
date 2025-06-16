from ultralytics import YOLO

# 1. 모델 불러오기
model = YOLO("yolov8n.pt")

# 2. 학습 실행
model.train(
    data="path_to_yaml",    # 학습 설정 YAML
    epochs=100,           # 학습 횟수
    imgsz=640,           # 입력 이미지 크기
    batch=16,            # 배치 크기
    name="project_name" # 결과 저장 디렉토리 이름
)
