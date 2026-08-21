import cv2
from ultralytics import YOLO

# -----------------------------
# ตั้งค่าระบบ
# -----------------------------
CAMERA_INDEX = 0

# โหลดโมเดล AI
model = YOLO("yolo11n.pt")

# เปิดกล้อง
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

print("เปิดกล้องสำเร็จ")
print("กด Q เพื่อออก")

while True:
    ret, frame = cap.read()

    if not ret:
        print("อ่านภาพจากกล้องไม่ได้")
        break

    # ขนาดภาพ
    height, width = frame.shape[:2]

    # จุดกึ่งกลางภาพ
    mid_x = width // 2
    mid_y = height // 2

    # --------------------------------
    # กำหนดพื้นที่ของโต๊ะ 4 ตัว
    # --------------------------------
    zones = {
        "A1": (0, 0, mid_x, mid_y),
        "A2": (mid_x, 0, width, mid_y),
        "B1": (0, mid_y, mid_x, height),
        "B2": (mid_x, mid_y, width, height)
    }

    # ให้ AI ตรวจจับคน
    results = model(
        frame,
        conf=0.45,
        classes=[0],
        verbose=False
    )

    # สถานะเริ่มต้น ทุกโต๊ะว่าง
    table_status = {
        "A1": False,
        "A2": False,
        "B1": False,
        "B2": False
    }

    # --------------------------------
    # ตรวจว่าคนอยู่โต๊ะไหน
    # --------------------------------
    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # จุดกึ่งกลางของคน
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # ตรวจว่าจุดกลางอยู่ในโซนไหน
            for table, (zx1, zy1, zx2, zy2) in zones.items():

                if (
                    zx1 <= center_x <= zx2
                    and
                    zy1 <= center_y <= zy2
                ):
                    table_status[table] = True

            # วาดกรอบคน
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 0),
                2
            )

    # --------------------------------
    # วาดโต๊ะ 4 ช่อง
    # --------------------------------
    for table, (x1, y1, x2, y2) in zones.items():

        if table_status[table]:
            status_text = "OCCUPIED"
        else:
            status_text = "FREE"

        # สีของกรอบ
        if table_status[table]:
            border_color = (0, 0, 255)       # แดง
        else:
            border_color = (0, 255, 0)       # เขียว

        # วาดกรอบโต๊ะ
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            border_color,
            4
        )

        # ชื่อโต๊ะ
        cv2.putText(
            frame,
            table,
            (x1 + 20, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            border_color,
            3
        )

        # สถานะ
        cv2.putText(
            frame,
            status_text,
            (x1 + 20, y1 + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            border_color,
            2
        )

    # แสดงภาพ
    cv2.imshow("Smart Table AI - Table Test", frame)

    # กด Q เพื่อออก
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()