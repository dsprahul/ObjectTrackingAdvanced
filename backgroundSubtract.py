import numpy as np
import cv2
import time
cap = cv2.VideoCapture(1) 
fgbg = cv2.BackgroundSubtractorMOG2()
while(1):
	
	_, frame = cap.read()
	fgmask = fgbg.apply(frame)
	cv2.imshow('frame',fgmask)

	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
