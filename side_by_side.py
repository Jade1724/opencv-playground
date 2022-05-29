import numpy as np
import cv2

# Two videos with the same dimentaion
cap1 = cv2.VideoCapture("./videos/vr-player.mp4")
cap2 = cv2.VideoCapture("./videos/vr-player-masked.mp4")

target_fps   = round(cap1.get(cv2.CAP_PROP_FPS))
frame_width  = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter("bg_subtraction_demo.mp4", cv2.VideoWriter_fourcc(*"mp4v"), target_fps, (frame_width // 2, frame_height //4))

while True:
    # Returns ret (if the capture worked properly) and frame (image itself in numpy array)
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # Get a width property and height property
    # Slice cannot accept float, so need to conver it to int
    width = int(cap1.get(3))
    height = int(cap1.get(4))

    # Create a blank canvas to show four images
    image = np.zeros((height // 4, width // 2, 3), np.uint8)
    # Shrink the image to one fourth size
    # The rotated dimension has to fit teh distination matrix segment in the image
    smaller_frame1 = cv2.resize(frame1, (0, 0), fx = 0.25, fy= 0.25)
    smaller_frame2 = cv2.resize(frame2, (0, 0), fx = 0.25, fy = 0.25)
    image[:, :width//4] = smaller_frame1
    image[:, width//4:] = smaller_frame2
    cv2.imshow('Frame', image)

    out.write(image)

    # Wait up to one millisecond and if q is pressed, end showing the video
    if cv2.waitKey(1) == ord('q'):
        break

cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()