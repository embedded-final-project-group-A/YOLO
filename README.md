# YOLO

# Model 설치
<pre>
<code>
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
pip install -e .
</code>
</pre>


# Data

- AIHUB에서 아래 데이터들 Download

### 1.실내(편의점,매장) 사람 이상행동 데이터

- 전도,흡연,절도,폭행 download

### 2.실내(편의점, 매장) 구매행동 데이터

- 매장이동,선택,구매 download

### 사용된 이미지 수
- 실내(편의점,매장) 사람 이상행동 데이터
    - train : 5322개
    - val : 658개
- 실내(편의점, 매장) 구매행동 데이터
    - train : 35119개
    - val : 4267개

# Train
- epoch : 100
- batch size : 16
- 사용한 pretrained model : yolov8n
    - 버전 : [Ultralytics YOLOv8 v8.0+](https://github.com/ultralytics/ultralytics)
    - 경량화된 YOLO 모델('yolov8n.pt')을 기반으로 학습

# Model Architecture
- **Backbone**: CSPDarkNet
- **Neck**: PAN-FPN
- **Head**: YOLO Detection Head
- **Activation**: SiLU (Sigmoid Linear Unit)


# 구현 및 모델 설계 특징

- 총 13개의 행동 클래스로 구성되며, 서로 다른 두 데이터셋을 통합하여 학습
- AIHub XML 라벨을 YOLO 형식으로 변환하는 전처리 파이프라인을 구축
- 영상(mp4)에서 10프레임 간격으로 이미지 추출하여 학습 데이터 구성
- `data.yaml` 파일은 13개 클래스를 기반으로 직접 작성
- 이미지 크기: 640x640, batch size: 16, epoch: 100
- YOLOv8 기본 anchor 설정(auto anchor) 사용
- 최종 모델은 `best.pt`로 저장되며, 이후 추론에 활용


# 모델 성능
![Confusion Matrix](result/yolov8_final_project/confusion_matrix.png)
![F1 Score](result/yolov8_final_project/F1_curve.png)
![Precision](result/yolov8_final_project/P_curve.png)
![Recall](result/yolov8_final_project/R_curve.png)
![Precision-Recall](result/yolov8_final_project/PR_curve.png)
![Others](result/yolov8_final_project/results.png)