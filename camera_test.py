import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

print("เปิดกล้องสำเร็จ")
print("กด Q เพื่อปิด")

while True:
    ret, frame = camera.read()

    if not ret:
        print("อ่านภาพจากกล้องไม่ได้")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()