from ultralytics import YOLO
import cv2

print("กำลังโหลด AI...")
model = YOLO("yolov8n.pt")
print("โหลด AI สำเร็จ")

# ใช้ DroidCam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("เปิดกล้องไม่ได้")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("อ่านภาพไม่ได้")
        break

    frame = cv2.resize(frame, (640, 480))

    results = model(frame, imgsz=320, verbose=False)

    people = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                people += 1

    cv2.putText(frame, f"People: {people}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Smart Table AI", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()