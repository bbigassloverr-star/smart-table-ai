import cv2

for i in range(5):
    print(f"กำลังทดสอบ Camera {i}")

    cap = cv2.VideoCapture(i)

    if cap.isOpened():
        ret, frame = cap.read()

        if ret and frame is not None:
            print(f"Camera {i} ใช้งานได้")

            cv2.imshow(f"Camera {i}", frame)
            key = cv2.waitKey(3000)  # แสดง 3 วินาที
            cv2.destroyAllWindows()
        else:
            print(f"Camera {i} เปิดได้แต่ภาพไม่ได้")
    else:
        print(f"Camera {i} เปิดไม่ได้")

    cap.release()

print("เสร็จแล้ว")