from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

# สถานะโต๊ะ
table_status = {
    "A1": "free"
}

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, imgsz=320)

    found_person = False

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                found_person = True

    # ถ้ามีคน → โต๊ะไม่ว่าง
    if found_person:
        table_status["A1"] = "occupied"
    else:
        table_status["A1"] = "free"

    print(table_status)

    cv2.imshow("Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()