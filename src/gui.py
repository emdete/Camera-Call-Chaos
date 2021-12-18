#!/usr/bin/env python3
from tkinter import Tk, StringVar, Label, Button, BOTH, PhotoImage, Frame, N, E, W, S, LEFT
from threading import Thread
from sys import argv
from processing import Processor

class State:
	def __init__(self):
		self.running = False
		self.recording = False
		self.glitch = False
		self.effect = 'normal'

def quit(*a):
	global processor, t
	processor.quit()
	t.join()
	app.quit()

def set_state(effect):
	global current_state, state
	current_state.set('Status: {}'.format(effect.capitalize().replace('_', ' ')))
	state.effect = effect
	if DEBUGGING: print(f'virtual camera to state {effect}')

def normalState():
	set_state('normal')

def corruptionState():
	set_state('jpeg_corruption')

def compressionState():
	set_state('jpeg_compression')

def lowPixelatedState():
	set_state('binary')

def oldMovieState():
	set_state('blurfilter')

def colorInvertState():
	set_state('edgeFilter')

def blurFilterState():
	set_state('waterfilter')

def animalFilterState():
	set_state('animalfilter')

def asciiartState():
	set_state('asciiart')

def recordStartState():
	current_state.set('Status: Aufzeichnen')
	state.recording = True
	state.glitch = False
	if DEBUGGING: print('state record')

def recordStopState():
	current_state.set('Status: Schleife')
	state.recording = False
	if DEBUGGING: print('recordStopState')

def goLiveState():
	set_state(state.effect)
	state.glitch = True
	if DEBUGGING: print('onRecordState')

DEBUGGING = False
for arg in argv[1:]:
	if arg == '-d' or arg == '--debug':
		DEBUGGING = True # enable debugging out
		print('Debugging log enabled')
	else:
		print('Unknown argument', arg)
if DEBUGGING: print('GUI init')
app = Tk()
for n in ('<Control-q>', '<Control-w>', '<Control-x>', '<Alt-F4>', 'q', ):
	app.bind_all(n, quit)
current_state = StringVar()
state = State()
normalState()
processor = Processor(state)
t = Thread(target=processor.run, daemon=True)
t.start()
app.title('Camera.Call.Chaos')
app.iconphoto(False, PhotoImage(file = 'favicon.png'))
if DEBUGGING: print('Creating widgets')
frame = Frame(app)
grid_defaults = dict(padx=4, pady=5, ipadx=2, ipady=2, sticky=N+S+W+E, )
widgets_defaults = dict(background='#30536b', border=0, foreground='#00f7ff', )
Button(frame, text='Normal', command=normalState, **widgets_defaults) .grid(row=0, column=0, **grid_defaults)
Button(frame, text='Korruption', command=corruptionState, **widgets_defaults) .grid(row=0, column=1, **grid_defaults)
Button(frame, text='Compression', command=compressionState, **widgets_defaults) .grid(row=0, column=2, **grid_defaults)
Button(frame, text='AsciiArt', command=asciiartState, **widgets_defaults) .grid(row=1, column=0, **grid_defaults)
Button(frame, text='Binary', command=lowPixelatedState, **widgets_defaults) .grid(row=1, column=1, **grid_defaults)
Button(frame, text='Blur', command=oldMovieState, **widgets_defaults) .grid(row=1, column=2, **grid_defaults)
Button(frame, text='Edge', command=colorInvertState, **widgets_defaults) .grid(row=2, column=0, **grid_defaults)
Button(frame, text='Animal Filter', command=animalFilterState, **widgets_defaults) .grid(row=2, column=1, **grid_defaults)
Button(frame, text='Water', command=blurFilterState, **widgets_defaults) .grid(row=2, column=2, **grid_defaults)
Button(frame, text='Aufzeichnung start', command=recordStartState, **widgets_defaults) .grid(row=3, column=0, **grid_defaults)
Button(frame, text='Aufzeichnung stop', command=recordStopState, **widgets_defaults) .grid(row=3, column=1, **grid_defaults) # TODO disable by flow
Button(frame, text='Zurück live', command=goLiveState, **widgets_defaults) .grid(row=3, column=2, **grid_defaults)
Label(frame, textvariable=current_state, justify=LEFT, border=2,
	#relief=RIDGE, background='#2654de', foreground='#fff',
	).grid(row=4, columnspan=3, **grid_defaults)
frame.pack(expand=1, fill=BOTH)
app.mainloop()

