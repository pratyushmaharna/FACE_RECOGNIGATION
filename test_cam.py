# import cv2

# video = cv2.VideoCapture(0)  # try 0 first

# if not video.isOpened():
#     print("Error: Webcam not accessible")
# else:
#     print("Webcam opened successfully")

# while True:
#     ret, frame = video.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     cv2.imshow("Test Camera", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()