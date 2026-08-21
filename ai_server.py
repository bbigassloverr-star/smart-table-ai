import cv2
import requests
import time
from ultralytics import YOLO

# -----------------------------
# ตั้งค่า
# -----------------------------
CAMERA_INDEX = 0
FLASK_URL = "https://smart-table-ai.onrender.com/api/update"

# ส่งข้อมูลไป Render ทุก 1 วินาที
last_update = 0
UPDATE_INTERVAL = 1.0

# ต้องพบ/ไม่พบต่อเนื่องกี่วินาที
DELAY_SECONDS = 5.0

# -----------------------------
# โหลด AI
# -----------------------------
model = YOLO("yolo11n.pt")

# -----------------------------
# เปิดกล้อง
# -----------------------------
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

print("AI Camera Started")
print("กด Q เพื่อออก")

# -----------------------------
# สถานะยืนยันแล้ว
# -----------------------------
stable_status = {
    "A1": "free",
    "A2": "free",
    "B1": "free",
    "B2": "free"
}

# -----------------------------
# ตัวจับเวลา
# -----------------------------
occupied_start = {
    "A1": None,
    "A2": None,
    "B1": None,
    "B2": None
}

free_start = {
    "A1": None,
    "A2": None,
    "B1": None,
    "B2": None
}

while True:

    ret, frame = cap.read()

    if not ret:
        print("อ่านภาพจากกล้องไม่ได้")
        break

    height, width = frame.shape[:2]

    mid_x = width // 2
    mid_y = height // 2

    # -----------------------------
    # พื้นที่โต๊ะ 4 ตัว
    # -----------------------------
    zones = {
        "A1": (0, 0, mid_x, mid_y),
        "A2": (mid_x, 0, width, mid_y),
        "B1": (0, mid_y, mid_x, height),
        "B2": (mid_x, mid_y, width, height)
    }

    # -----------------------------
    # สถานะจาก AI รอบปัจจุบัน
    # -----------------------------
    raw_status = {
        "A1": "free",
        "A2": "free",
        "B1": "free",
        "B2": "free"
    }

    # -----------------------------
    # YOLO ตรวจจับคน
    # -----------------------------
    results = model(
        frame,
        conf=0.45,
        classes=[0],
        verbose=False
    )

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # ตรวจว่าคนอยู่ในโต๊ะไหน
            for table, (zx1, zy1, zx2, zy2) in zones.items():

                if (
                    zx1 <= center_x <= zx2
                    and
                    zy1 <= center_y <= zy2
                ):
                    raw_status[table] = "occupied"

            # วาดกรอบคน
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 0),
                2
            )

    # -----------------------------
    # ระบบ Delay 5 วินาที
    # -----------------------------
    current_time = time.time()

    for table in zones:

        # -------------------------
        # กรณี AI พบคน
        # -------------------------
        if raw_status[table] == "occupied":

            # ไม่พบคนต่อเนื่อง -> ล้าง timer free
            free_start[table] = None

            # ถ้ายังเป็น free ให้เริ่มจับเวลา
            if stable_status[table] == "free":

                if occupied_start[table] is None:
                    occupied_start[table] = current_time

                # ครบ 5 วินาที
                elif current_time - occupied_start[table] >= DELAY_SECONDS:
                    stable_status[table] = "occupied"
                    occupied_start[table] = None

            else:
                # เป็น occupied อยู่แล้ว
                occupied_start[table] = None

        # -------------------------
        # กรณี AI ไม่พบคน
        # -------------------------
        else:

            # พบคนต่อเนื่อง -> ล้าง timer occupied
            occupied_start[table] = None

            # ถ้ายังเป็น occupied ให้เริ่มจับเวลา
            if stable_status[table] == "occupied":

                if free_start[table] is None:
                    free_start[table] = current_time

                # ครบ 5 วินาที
                elif current_time - free_start[table] >= DELAY_SECONDS:
                    stable_status[table] = "free"
                    free_start[table] = None

            else:
                # เป็น free อยู่แล้ว
                free_start[table] = None

    # -----------------------------
    # ส่งสถานะไป Render ทุก 1 วินาที
    # -----------------------------
    if current_time - last_update >= UPDATE_INTERVAL:

        try:

            response = requests.post(
                FLASK_URL,
                json=stable_status,
                timeout=5
            )

            print(
                "ส่งสถานะ:",
                stable_status,
                "→",
                response.status_code
            )

            last_update = current_time

        except requests.RequestException as e:

            print(
                "ส่งข้อมูลไม่สำเร็จ:",
                e
            )

    # -----------------------------
    # แสดงกรอบโต๊ะ
    # -----------------------------
    for table, (x1, y1, x2, y2) in zones.items():

        occupied = stable_status[table] == "occupied"

        if occupied:
            color = (0, 0, 255)
            text = "OCCUPIED"
        else:
            color = (0, 255, 0)
            text = "FREE"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            4
        )

        cv2.putText(
            frame,
            f"{table}: {text}",
            (x1 + 20, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    # -----------------------------
    # แสดงภาพ
    # -----------------------------
    cv2.imshow(
        "Smart Table AI",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()