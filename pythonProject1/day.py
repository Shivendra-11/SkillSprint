import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480
cap.set(3, frame_width)
cap.set(4, frame_height)


def empty(x):
    pass


cv2.namedWindow("parameters")
cv2.createTrackbar("threshold1", "parameters", 100, 225, empty)
cv2.createTrackbar("threshold2", "parameters", 200, 225, empty)


def get_contours(img_dilate, img_contours):
    contours,hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

for cnt in contours:
        area_min=cv2.contourArea(cnt)
        cv2.drawContours(img_contours,cnt,-1,(0,255,0),3)
        peri=cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,0.02*peri,True)
        x,y,w,h=cv2.boundingRect(approx)
        cv2.rectangle(img_contours,(x,y),(x+w,y+h),(255,0,255),3)
        cv2.putText(img_contours,"Points"+str(len(approx)),(x,y),(x+w,y+h),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2,0)
        cv2.putText(img_contours,'Area:'+str(int(area_min)),(x+w+45,y+h+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2,0)

while True:
    ret, img = cap.read()
    img_contours = img.copy()  # Corrected the function call

    img_blur = cv2.GaussianBlur(img, (7, 7), 0)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

    t1 = cv2.getTrackbarPos("threshold1", "parameters")
    t2 = cv2.getTrackbarPos("threshold2", "parameters")

    img_canny = cv2.Canny(img_gray, t1, t2)
    kernel = np.ones((5, 5), np.uint8)
    img_dilate = cv2.dilate(img_canny, kernel, iterations=1)

    get_contours(img_dilate, img_contours)

    output = np.hstack([img_gray, img_canny, img_dilate])
    cv2.imshow("Output", output)

    cv2.imshow("parameters", img_contours)  # Show contours in the "parameters" window

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
