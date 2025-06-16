# 238-1
import os
import cv2
import xml.etree.ElementTree as ET

# 설정
XML_DIR = "path_to_이상행동 데이터_label_data"             # XML 라벨 디렉토리
VIDEO_DIR = "path_to_이상행동 데이터_mp4_data"                # mp4 영상 디렉토리
OUTPUT_LABEL_DIR = "path_to_store_label_data"   # YOLO 라벨 저장 디렉토리
OUTPUT_IMG_DIR = "path_to_store_image_data"     # 프레임 이미지 저장 디렉토리
IMG_WIDTH = 1920
IMG_HEIGHT = 1080

os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

#클래스 매핑 (8종)
CLASS_MAP = {
    "fall_start": 0, "fall_end": 1,
    "theft_start": 2, "theft_end": 3,
    "smoke_start": 4, "smoke_end": 5,
    "fight_start": 6, "fight_end": 7
}


# XML 반복
for xml_file in os.listdir(XML_DIR):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(XML_DIR, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    base_name = os.path.splitext(xml_file)[0]  # ex: C_3_7_1_..._F2

    frame_label_dict = {}

    for track in root.findall("track"):
        label = track.attrib["label"]
        if label not in CLASS_MAP:
            continue
        class_id = CLASS_MAP[label]

        for box in track.findall("box"):
            if box.attrib.get("outside") == "1":
                continue

            frame = int(box.attrib["frame"])
            xtl = float(box.attrib["xtl"])
            ytl = float(box.attrib["ytl"])
            xbr = float(box.attrib["xbr"])
            ybr = float(box.attrib["ybr"])

            x_center = (xtl + xbr) / 2 / IMG_WIDTH
            y_center = (ytl + ybr) / 2 / IMG_HEIGHT
            width = (xbr - xtl) / IMG_WIDTH
            height = (ybr - ytl) / IMG_HEIGHT

            line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            frame_label_dict.setdefault(frame, []).append(line)

    # 연결된 mp4 파일 열기
    video_file = base_name + ".mp4"
    video_path = os.path.join(VIDEO_DIR, video_file)
    if not os.path.exists(video_path):
        print(f"[경고] {video_file} 없음")
        continue

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_num, labels in frame_label_dict.items():
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            print(f"[오류] {video_file}의 프레임 {frame_num} 추출 실패")
            continue

        # 저장 이름
        filename = f"{base_name}_{frame_num:04d}"
        img_path = os.path.join(OUTPUT_IMG_DIR, filename + ".jpg")
        label_path = os.path.join(OUTPUT_LABEL_DIR, filename + ".txt")

        cv2.imwrite(img_path, frame)
        with open(label_path, 'w') as f:
            f.writelines(labels)

    cap.release()
    print(f"[완료] {xml_file} 처리됨")


# 238-1 -> 이미지 너무 많아서 프레임 조정
import os
import cv2
import xml.etree.ElementTree as ET

# 설정
XML_DIR = "path_to_구매행동 데이터_label_data"             # XML 라벨 디렉토리
VIDEO_DIR = "path_to_구매행동 데이터_mp4_data"                # mp4 영상 디렉토리
OUTPUT_LABEL_DIR = "path_to_store_label_data"   # YOLO 라벨 저장 디렉토리
OUTPUT_IMG_DIR = "path_to_store_image_data"     # 프레임 이미지 저장 디렉토리
IMG_WIDTH = 1920
IMG_HEIGHT = 1080
FRAME_GAP = 30  # 프레임 간격 설정

os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

# 클래스 매핑 (5종)
CLASS_MAP = {
    "moving": 8,
    "select_start": 9,
    "select_end": 10,
    "buying_start": 11,
    "buying_end": 12
}

# XML 반복
for xml_file in os.listdir(XML_DIR):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(XML_DIR, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    base_name = os.path.splitext(xml_file)[0]  # ex: C_3_7_1_..._F2

    frame_label_dict = {}
    last_saved = {}  # 클래스별 마지막 저장된 프레임

    for track in root.findall("track"):
        label = track.attrib["label"]
        if label not in CLASS_MAP:
            continue
        class_id = CLASS_MAP[label]

        for box in track.findall("box"):
            if box.attrib.get("outside") == "1":
                continue

            frame = int(box.attrib["frame"])

            # 프레임 간격 제한
            if label in last_saved and abs(frame - last_saved[label]) < FRAME_GAP:
                continue

            xtl = float(box.attrib["xtl"])
            ytl = float(box.attrib["ytl"])
            xbr = float(box.attrib["xbr"])
            ybr = float(box.attrib["ybr"])

            x_center = (xtl + xbr) / 2 / IMG_WIDTH
            y_center = (ytl + ybr) / 2 / IMG_HEIGHT
            width = (xbr - xtl) / IMG_WIDTH
            height = (ybr - ytl) / IMG_HEIGHT

            line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            frame_label_dict.setdefault(frame, []).append(line)

            last_saved[label] = frame  # 마지막 저장된 프레임 업데이트

    # 연결된 mp4 파일 열기
    video_file = base_name + ".mp4"
    video_path = os.path.join(VIDEO_DIR, video_file)
    if not os.path.exists(video_path):
        print(f"[경고] {video_file} 없음")
        continue

    cap = cv2.VideoCapture(video_path)

    for frame_num, labels in frame_label_dict.items():
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            print(f"[오류] {video_file}의 프레임 {frame_num} 추출 실패")
            continue

        # 저장 이름
        filename = f"{base_name}_{frame_num:04d}"
        img_path = os.path.join(OUTPUT_IMG_DIR, filename + ".jpg")
        label_path = os.path.join(OUTPUT_LABEL_DIR, filename + ".txt")

        cv2.imwrite(img_path, frame)
        with open(label_path, 'w') as f:
            f.writelines(labels)

    cap.release()
    print(f"[완료] {xml_file} 처리됨")