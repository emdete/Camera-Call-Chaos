#!/usr/bin/env python3
from tkinter import *
import threading
import sys
from main import run

class State:
	recording = False
	glitch = False
	filter = ""

def quit(*a):
	global t
	t.join()
	app.quit()

def normalState():
	CurrentState.set("Kamerastand: Normal")
	state.filter = ""
	if DEBUGGING:
		print("virtualCamera is back on Normal State")

def corruptionState():
	CurrentState.set("Kamerastand: corruption")
	state.filter = "jpeg_corruption"
	if DEBUGGING:
		print("glitching through the camera (epilepsy warning)")

def compressionState():
	CurrentState.set("Kamerastand: JPEG compression")
	state.filter = "jpeg_compression"
	if DEBUGGING:
		print("virtualCamera has now the default pixeled state")

def lowPixelatedState():
	CurrentState.set("Kamerastand: Binary")
	state.filter = "binary"
	if DEBUGGING:
		print("virtualCamera has now the low pixeled state")

def oldMovieState():
	CurrentState.set("Kamerastand: Blur Filter")
	state.filter = "blurfilter"
	if DEBUGGING:
		print("setting virtualCamera filter as \"old movie\"")

def colorInvertState():
	CurrentState.set("Kamerastand: Edge Filter")
	state.filter = "edgeFilter"
	if DEBUGGING:
		print("inverting colors on virtualCamera")

def blurFilterState():
	CurrentState.set("Kamerastand: Water Filter")
	state.filter = "waterfilter"
	if DEBUGGING:
		print("blurFilterState")

def animalFilterState():
	CurrentState.set("Kamerastand: Animal Filter")
	state.filter = "animalfilter"
	if DEBUGGING:
		print("animalfilter")

def asciiartState():
	CurrentState.set("Kamerastand: ASCII-Effekt")
	state.filter = "asciiart"
	if DEBUGGING:
		print("onAsciiState")

def recordStartState():
	CurrentState.set("Kamerastand: Aufzeichnen")
	state.recording = True
	state.glitch = False
	if DEBUGGING:
		print("recordStartState")

def recordStopState():
	CurrentState.set("Kamerastand: Loop")
	state.recording = False
	if DEBUGGING:
		print("recordStopState")

def goLiveState():
	CurrentState.set("Kamerastand: Live")
	state.glitch = True
	if DEBUGGING:
		print("onRecordState")

def spinnerChangeListener(value):
	spinnerValue = value
	if DEBUGGING:
		print("Spinner Value = " + str(spinnerValue))

def refreshRateChanger():
	EFFECT_REFRESH_RATE = numberPickerSelection.get()
	if DEBUGGING:
		print("Effect Refresh Rate = " + str(EFFECT_REFRESH_RATE))

DEBUGGING = False
RESIZEABLE = False
# GUI init
app = Tk()
for n in ('<Control-q>', '<Control-w>', '<Control-x>', '<Alt-F4>', 'q', ):
	app.bind_all(n, quit)
windowWidth = 650
windowHeight = 450
spinnerValue = 1
EFFECT_REFRESH_RATE = 1
numberPickerSelection = IntVar()
spinnerSelection = IntVar()
WINDOW_BACKGROUND_COLOR = "#10286e"
BUTTON_BACKGROUND_COLOR = "#30536b"
TEXT_COLOR = "#00f7ff"
LABEL_BACKGROUND = "#2654de"
windowGeo = (str(windowWidth) + "x" + str(windowHeight))
CurrentState = StringVar()
CurrentState.set("Kamerastand: Normal")
currentState = Label(app)
spinner_blurFilter = Scale(app)
numberPicker = Spinbox(app)
state = State()
# Window-Größe: (Horizontale Größe x Vertikale Größe)
t = threading.Thread(target=run, daemon=True, args=(state,))
t.start()
for arg in sys.argv[1:]:
	if arg == "-d" or arg == '--debug':
		# enable debugger
		DEBUGGING = True
	elif arg == "-r" or arg == '--resizeable':
		RESIZEABLE = True
if DEBUGGING:
	print("creating window with favicon \"favicon.png\" and its window geometry on " + windowGeo)
app.title("Camera.Call.Chaos")
app.geometry(windowGeo)
faviconImg = PhotoImage(file = "favicon.png")
app.iconphoto(False, faviconImg)
if DEBUGGING:
	print("Assigning Widgets")
currentState = Label(app, textvariable = CurrentState, background = LABEL_BACKGROUND, foreground = "#fff")
currentState.place(x = 1, y = 1)

btn_normalState = Button(app, text = "Normale Kamera", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = normalState)
btn_normalState.place(x = 10, y = 30)

btn_jpeg_corruption = Button(app, text = "corruption", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = corruptionState)
btn_jpeg_corruption.place(x = 147, y = 30)

btn_pixelState = Button(app, text = "JPEG compression", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = compressionState)
btn_pixelState.place(x = 300, y = 30)

btn_highPixeled = Button(app, text = "ASCII", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = asciiartState)
btn_highPixeled.place(x = 500, y = 30)

btn_oldMovie = Button(app, text = "Binary", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = lowPixelatedState)
btn_oldMovie.place(x = 10, y = 70)

btn_colorInvert = Button(app, text = "Blur", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = oldMovieState)
btn_colorInvert.place(x = 90, y = 70)

btn_lowPixeled = Button(app, text = "Edge", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = colorInvertState)
btn_lowPixeled.place(x = 170, y = 70)

btn_blurFilter = Button(app, text = "Animal Filter", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = animalFilterState)
btn_blurFilter.place(x = 330, y = 70)

btn_blurFilter = Button(app, text = "Water", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = blurFilterState)
btn_blurFilter.place(x = 230, y = 70)

# spinner_blurFilter = Scale(app, from_ = 1, to = 100, length = 142, orient = HORIZONTAL, command = spinnerChangeListener)
# spinner_blurFilter.place(x = 407, y = 98)
#
# label0 = Label(app, text = "Bildwiederholfrequenz für Kameraeffekte (jede Sekunden):", border = 0, background = LABEL_BACKGROUND, foreground = "#fff")
# label0.place(x = 0, y = 170)
#
# numberPicker = Spinbox(app, textvariable = numberPickerSelection, from_ = 1, to = 60, width = 3, command = refreshRateChanger)
# numberPicker.place(x = 340, y = 168)

btn_normalState = Button(app, text = "Aufzeichnung starten", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = recordStartState)
btn_normalState.place(x = 0, y = 200)

btn_normalState = Button(app, text = "Aufzeichnung stoppen", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = recordStopState)
btn_normalState.place(x = 200, y = 200)

btn_normalState = Button(app, text = "Live gehen", border = 0, background = BUTTON_BACKGROUND_COLOR, foreground = TEXT_COLOR, command = goLiveState)
btn_normalState.place(x = 400, y = 200)

app.resizable(RESIZEABLE, RESIZEABLE)
app.mainloop()

