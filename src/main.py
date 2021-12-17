import pyvirtualcam
import numpy as np
import cv2 as cv
import os
import torch
from Filter.jpeg_artifacts import jpeg_corruption, jpeg_compression
from Filter.animalfilter import animalfilter
from Filter.Ascii import ascii
from Filter.binary import binary
from Filter.blurfilter import blurfilter
from Filter.edgeFilter import edgeFilter
from Filter.pixelError import pixelError
from Filter.waterfilter import waterfilter
from loop import loop

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
filters = dict(
	animalfilter=animalfilter,
	jpeg_compression=jpeg_compression,
	jpeg_corruption=jpeg_corruption,
	ascii=ascii,
	binary=binary,
	blurfilter=blurfilter,
	edgeFilter=edgeFilter,
	pixelError=pixelError,
	waterfilter=waterfilter,
	)

def run(state):
	capture = cv.VideoCapture(os.environ["WEBCAM_INDEX"] if "WEBCAM_INDEX" in os.environ else 0)
	fmt = pyvirtualcam.PixelFormat.BGR
	width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

	with pyvirtualcam.Camera(width, height, 20, fmt=fmt, device="/dev/video2") as cam:
		print(f'Using virtual camera: {cam.device}')
		while True:
			isTrue, frame = capture.read()
			frame = np.flip(frame, axis=1)
			frame = loop(frame, state.recording, state.glitch)
			frame = filters.get(state.filter, lambda f:f)(frame, model=model, width=width, height=height)
			cam.send(frame)
			cam.sleep_until_next_frame()
	capture.release()
	cv.destroyAllWindows()
