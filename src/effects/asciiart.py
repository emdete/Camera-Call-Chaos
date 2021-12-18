import cv2
import numpy as np

def _asciiart(frames, width, height, gscale, **argv):
	resized_img = cv2.resize(cv2.cvtColor(cv2.cvtColor(frames, cv2.COLOR_BGR2HSV), cv2.COLOR_BGR2GRAY),(200,100))
	scale = len(gscale)/255
	frame = np.zeros((height, width, 3), dtype = "uint8")
	y = 0
	for row in resized_img:
		x = 0
		for idx in row * scale:
			frame = cv2.putText(frame, gscale[int(idx)], (x, y, ), cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 255, 0, 255), 1)
			x += 8
		y += 10
	return frame

def asciiart_binary(frames, width, height, gscale="01", **argv):
	return _asciiart(frames, width, height, gscale, **argv)

def asciiart(frames, width, height, gscale="@%#*+=-:. ", **argv):
	return _asciiart(frames, width, height, gscale, **argv)

