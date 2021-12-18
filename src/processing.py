from pyvirtualcam import PixelFormat, Camera
from numpy import flip
import cv2 as cv
from os import environ
from torch import hub
from effects.jpeg_artifacts import jpeg_corruption, jpeg_compression
from effects.animalfilter import animalfilter
from effects.asciiart import asciiart, asciiart_binary
from effects.blurfilter import blurfilter
from effects.edgeFilter import edgeFilter
from effects.pixelError import pixelError
from effects.waterfilter import waterfilter
from effects.jpeg_artifacts import jpeg_corruption

class Processor(object):
	def __init__(self, state):
		self.state = state
		self.frames = []
		self.current_frame = 0
		self.frame_count = 0
		self.forward = False
		self.model = hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
		self.effects = dict(
			animalfilter=animalfilter,
			compression=jpeg_compression,
			corruption=jpeg_corruption,
			asciiart=asciiart,
			asciiart_binary=asciiart_binary,
			blurfilter=blurfilter,
			edge=edgeFilter,
			pixelError=pixelError,
			waterfilter=waterfilter,
			)

	def process(self, frame, rec, glitch):
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
		self.state.running = False

	def run(self):
		try:
			self.state.running = True
			capture = cv.VideoCapture(int(environ.get("WEBCAM_INDEX", 0)))
			width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
			height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
			with Camera(
				width=width,
				height=height,
				fps=20,
				fmt=PixelFormat.BGR,
				device=environ.get("WEBCAM_DEVICE", "/dev/video2"),
				#print_fps=True,
				backend='v4l2loopback',
			) as cam:
				print('Using virtual camera:', cam.device)
				while self.state.running:
					isTrue, frame = capture.read()
					frame = flip(frame, axis=1)
					frame = self.process(frame, self.state.recording, self.state.glitch)
					if self.state.effect in self.effects:
						frame = self.effects[self.state.effect](frame, model=self.model, width=width, height=height)
					cam.send(frame)
					cam.sleep_until_next_frame()
			capture.release()
			cv.destroyAllWindows()
		except Exception as e:
			print('Error', e)
		finally:
			print('Processing-thread terminating')

