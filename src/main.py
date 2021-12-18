from pyvirtualcam import PixelFormat, Camera
from numpy import flip
import cv2 as cv
from os import environ
from torch import hub
from effects.jpeg_artifacts import jpeg_corruption, jpeg_compression
from effects.animalfilter import animalfilter
from effects.asciiart import asciiart
from effects.binary import binary
from effects.blurfilter import blurfilter
from effects.edgeFilter import edgeFilter
from effects.pixelError import pixelError
from effects.waterfilter import waterfilter
from effects.jpeg_artifacts import jpeg_corruption

class Processor(object):
	def __init__(self, state):
		self.running = True
		self.frames = []
		self.current_frame = 0
		self.frame_count = 0
		self.forward = False
		self.model = hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
		self.filters = dict(
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

	def __process(self, frame, rec, glitch):
		if rec:
			self.frames.append(frame)
			self.current_frame = len(self.frames) - 1
			return frame
		elif self.frames:
			if glitch:
				self.frame_count+=1
				if self.frame_count < 5:
					return jpeg_corruption(frame)
				self.frame_count = 0
				self.frames = []
				self.forward = False
				return frame
			else:
				self.current_frame += 1 if self.forward else -1
				if self.current_frame - 1 <= 0 or self.current_frame >= len(self.frames):
					self.forward = not self.forward
				return self.frames[self.current_frame - 1]
		else:
			return frame

	def quit(self):
		self.running = False

	def run(self):
		try:
			capture = cv.VideoCapture(int(environ.get("WEBCAM_INDEX", 0)))
			width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
			height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
			with Camera(
				width=width,
				height=height,
				fps=20,
				fmt=PixelFormat.BGR,
				device=environ.get("WEBCAM_DEVICE", "/dev/video2"),
				backend='v4l2loopback',
			) as cam:
				print(f'Using virtual camera: {cam.device}')
				while self.running:
					isTrue, frame = capture.read()
					frame = flip(frame, axis=1)
					frame = __process(frame, state.recording, state.glitch)
					if state.filter in self.filters:
						frame = self.filters[state.filter](frame, model=self.model, width=width, height=height)
					cam.send(frame)
					cam.sleep_until_next_frame()
			capture.release()
			cv.destroyAllWindows()
		finally:
			print('Processing-thread terminating')

def run(state):
	Processor(state).run()

