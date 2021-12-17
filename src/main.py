import pyvirtualcam
import numpy as np
import cv2 as cv
import os
import torch
from effects.jpeg_artifacts import jpeg_corruption, jpeg_compression
from effects.animalfilter import animalfilter
from effects.asciiart import asciiart
from effects.binary import binary
from effects.blurfilter import blurfilter
from effects.edgeFilter import edgeFilter
from effects.pixelError import pixelError
from effects.waterfilter import waterfilter
from loop import loop

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
filters = dict(
	animalfilter=animalfilter,
	jpeg_compression=jpeg_compression,
	jpeg_corruption=jpeg_corruption,
	asciiart=asciiart,
	binary=binary,
	blurfilter=blurfilter,
	edgeFilter=edgeFilter,
	pixelError=pixelError,
	waterfilter=waterfilter,
	)
further = True

def run(state):
	global filters, model, further
	capture = cv.VideoCapture(os.environ["WEBCAM_INDEX"] if "WEBCAM_INDEX" in os.environ else 0)
	width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
	with pyvirtualcam.Camera(
		width=width,
		height=height,
		fps=20,
		fmt=pyvirtualcam.PixelFormat.BGR,
		device="/dev/video2",
		backend='v4l2loopback',
	) as cam:
		print(f'Using virtual camera: {cam.device}')
		while further:
			isTrue, frame = capture.read()
			frame = np.flip(frame, axis=1)
			frame = loop(frame, state.recording, state.glitch)
			if state.filter in filters:
				frame = filters[state.filter](frame, model=model, width=width, height=height)
			cam.send(frame)
			cam.sleep_until_next_frame()
	capture.release()
	cv.destroyAllWindows()

