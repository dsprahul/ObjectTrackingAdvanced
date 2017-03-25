import numpy as np
import cv2
import time

cap = cv2.VideoCapture(1) 
fgbg = cv2.BackgroundSubtractorMOG2()

# Initial Value info of the ball. We need initial area and centroid 
# information based on HSV values of the ball

print "Hold the ball for 3 seconds"
time.sleep(2.5)

# Hoping for a stabilized image here...
print "Capturing ..."
_, frame = cap.read()

# RGB to HSV
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
# Calculating mask from hsv
mask = cv2.inRange(hsv,lower_colour, upper_colour)
	
# Finding contours to find Moments & Centroid
contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)



# Initializing area parameter and its corresponding contour, named 'contour_max'
area_max = 0

###### !!!!Computational Burden!!!! You'll improve this somehow. #######
for h,cnt in enumerate(contours):
	# Finding area of each contour and picking up the one with max area.
	area = cv2.contourArea(cnt)
	if (area > area_max) :
		area_max = area
		contour_max = cnt

			
# Finding centroid of that cue.
	
	
	
M = cv2.moments(contour_max)
	
past_x,past_y = centroid_x,centroid_y
centroid_x = int(M['m10']/M['m00'])
centroid_y = int(M['m01']/M['m00'])

# Initial parameters that will be supplied to foreground tracking algo.
(area_ball,InitialCentroidX,InitialCentroidY) = (area_max,centroid_x,centroid_y)

while(1):
	
	_, frame = cap.read()
	fgmask = fgbg.apply(frame)
	cv2.imshow('frame',fgmask)

	
	# Calculating mask from hsv
	mask = fgmask
	
	# Finding contours to find Moments & Centroid
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)





	###### !!!!Computational Burden!!!! You'll improve this somehow. #######
	counter=0
	for h,cnt in enumerate(contours):
		
		# Finding centroids & areas of all objects.
		M = cv2.moments(cnt)
		centroid_x[counter] = int(M['m10']/M['m00'])
		centroid_y[counter] = int(M['m01']/M['m00'])
		area[counter] = cv2.contourArea(cnt)
		counter +=1

	# Now we have centroids & areas of all objects in foreground. 
	# Lets match them with initial parameters to pinpoint ball

	# Area filter
	index = -1
	for value in area:
		index +=1
		count = -1
		if ((value < area_ball+area_threshold) and  (value > area_ball-area_threshold)) :
			count +=1
			ProbablyObject_area[count] = index
		else :
			pass
		
	# Coordinate filter for objects that passed Area filter
	indexC = -1
	for value in centroid_x:
		indexC +=1
		count = -1	
		if ((value < InitialCentroidX+InitialCentroidX_threshold) and  (value > InitialCentroidX-InitialCentroidX_threshold)) :
			count +=1
			ProbablyObject_InitialCentroidX[count] = indexC
		else :
			pass
	indexC = -1
	for value in centroid_y:
		indexC +=1
		count = -1	
		if ((value < InitialCentroidY+InitialCentroidY_threshold) and  (value > InitialCentroidY-InitialCentroidY_threshold)) :
			count +=1
			ProbablyObject_InitialCentroidY[count] = indexC
		else :
			pass

	
	# Permorming CentroidX AND CentroidY results
	centroid = set(centroidX).intersection(set(centroidY))
	ProbablyObject_centroid = list(centroid)


	## Okay cool, now ProbablyObject_XXXX arrarys will have index of our object of interest 
	## along with some other objects indices. Optimistically, AND of Area and Centroid probabilities 
	## should result in single result, if not, lets choose the first one.
	objecto = set(ProbablyObject_centroid).intersection(set(ProbablyObject_area))

	indexo = objecto[0]
	
	cv2.circle(frame,(centroid_x[indexo],centroid_y[indexo]),4,(0,255,255),-1) 
	cv2.imshow('Tracked',frame)

	### First iteration complete. Now, use Kalman filter to update Area and Coordinate info to track
	### object in next frame using same logic.	

	k = cv2.waitKey(30) & 0xff
	
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
