import cv2

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

print("Camera opened:", cap.isOpened())

if not cap.isOpened():
    print("Camera could not open!")
    exit()

while True:
    print("Reading camera frame...")

    success, frame = cap.read()

    if not success:
        print("Frame capture failed!")
        break

    cv2.imshow("Camera Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Camera test completed!")