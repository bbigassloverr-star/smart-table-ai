import cv2
import requests
from ultralytics import YOLO
import time

CAMERA_INDEX = 0
FLASK_URL = "https://smart-table-ai.onrender.com/api/update"
last_update = 0
UPDATE_INTERVAL = 1.0

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

print("AI Camera Started")
print("กด Q เพื่อออก")

while True:
    ret, frame = cap.read()

    if not ret:
        print("อ่านภาพจากกล้องไม่ได้")
        break

    height, width = frame.shape[:2]

    mid_x = width // 2
    mid_y = height // 2

    zones = {
        "A1": (0, 0, mid_x, mid_y),
        "A2": (mid_x, 0, width, mid_y),
        "B1": (0, mid_y, mid_x, height),
        "B2": (mid_x, mid_y, width, height)
    }

    results = model(
        frame,
        conf=0.45,
        classes=[0],
        verbose=False
    )

    table_status = {
        "A1": "free",
        "A2": "free",
        "B1": "free",
        "B2": "free"
    }

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            for table, (zx1, zy1, zx2, zy2) in zones.items():

                if (
                    zx1 <= center_x <= zx2
                    and
                    zy1 <= center_y <= zy2
                ):
                    table_status[table] = "occupied"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 0),
                2
            )
    # ส่งสถานะ AI ไป Flask
    current_time = time.time()

    if current_time - last_update >= UPDATE_INTERVAL:
        try:
            response = requests.post(
                FLASK_URL,
                json=table_status,
                timeout=5
            )

            print(
                "ส่งสถานะ:",
                table_status,
                "→",
                response.status_code
            )

            last_update = current_time

        except requests.RequestException as e:
            print("ส่งข้อมูลไม่สำเร็จ:", e)

    # วาดสถานะโต๊ะ
    for table, (x1, y1, x2, y2) in zones.items():

        occupied = table_status[table] == "occupied"

        color = (0, 0, 255) if occupied else (0, 255, 0)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            4
        )

        cv2.putText(
            frame,
            f"{table}: {table_status[table]}",
            (x1 + 20, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("Smart Table AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()