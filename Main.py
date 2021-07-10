import numpy as np
import cv2 as cv
video = 'C:\\Users\\tead1\Documents\\GitHub\\1st_cam_Maker\\izone-panorama_Trim.mp4'
cap = cv.VideoCapture(video)
# 너비, 높이
output_size = (180,333)
# 영상저장 하기 형식은 mp4
fourcc = cv.VideoWriter_fourcc('m','p','4','v')
# out = 결과물 이름을 video에 쓴 이름에서 따와서 넣음 
out =cv.VideoWriter('%s_output.mp4' % (video.split('.')[0]),fourcc, cap.get
(cv.CAP_PROP_FPS), output_size)
if not cap.isOpened():
    exit()


tracker = cv.TrackerCSRT_create()


ret, img = cap.read()

#추적하는 사각형 윈도우를 만들자
cv.namedWindow('SelectWindow')
cv.imshow('SelectWindow',img)
## setting ROI
rect = cv.selectROI('SelectWindow', img, showCrosshair=True, fromCenter=True)
cv.destroyWindow('SelectWindow')

#tracker 초기화
tracker.init(img,rect)


while True :
    ret, img = cap.read()
    if not ret:
        exit() 
    sucess, box = tracker.update(img)

    
    left, top, w,h = [int(v) for v in box]
    
    center_x = left + w /2
    center_y = top + h/2
# opencv에선 왼쪽위로 가면 -를 오른쪽 아래로 가면 +를 해줘야한다
    result_top = int(center_y - output_size[1] /2) 
    result_bottom = int(center_y + output_size[1] /2) 
    result_left = int(center_x - output_size[0] /2 )
    result_right = int(center_x + output_size[0] /2 )

    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)
    cv.rectangle(img, pt1=(left, top),pt2= (left+w, top+ h), color = (255,255,255), thickness= 10)
    cv.imshow('result_img',result_img)
    cv.imshow('img',img)
    if cv.waitKey(1) == ord('p'):
        break

