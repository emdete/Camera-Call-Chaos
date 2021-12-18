#!/usr/bin/env python3
from tkinter import Tk, StringVar, Label, Button, BOTH, PhotoImage, Frame, N, E, W, S, LEFT
from threading import Thread
from sys import argv
from processing import Processor

def quit(*a):
	'function to quit the program, end the thread, wait for it and terminate tk'
	global processor, t
	processor.quit()
	t.join()
	app.quit()

def set_state(effect):
	'set desired effect state'
	global current_state, processor
	current_state.set('Status: {}'.format(effect.capitalize().replace('_', ' ')))
	processor.effect = effect
	if DEBUGGING: print(f'virtual camera to {effect}')

def record_start():
	'start recording'
	global processor
	current_state.set('Status: Aufzeichnen')
	processor.recording = True
	processor.glitch = False
	if DEBUGGING: print('start record')

def record_stop():
	'stop recording'
	global processor
	current_state.set('Status: Schleife')
	processor.recording = False
	if DEBUGGING: print('stop record')

def record_live():
	'stop loop and go back to live'
	global processor
	set_state(processor.effect)
	processor.glitch = True
	if DEBUGGING: print('go live')

class Command(object):
	'class to create callable objects that contain arguments to a function - tk doesnt provide arguments to commands'
	def __init__(self, command, *args, **argv):
		self.command, self.args, self.argv = command, args, argv

	def __call__(self):
		self.command(*self.args, **self.argv)

DEBUGGING = False
# parse program arguments
for arg in argv[1:]:
	if arg == '-d' or arg == '--debug':
		DEBUGGING = True # enable debugging out
		print('Debugging log enabled')
	else:
		print('Unknown argument', arg)
if DEBUGGING: print('GUI init')
app = Tk()
app.title('Camera.Call.Chaos')
app.iconphoto(False, PhotoImage(file = 'favicon.png'))
# bind keys to terminate program
for n in ('<Control-q>', '<Control-w>', '<Control-x>', '<Alt-F4>', 'q', ):
	app.bind_all(n, quit)
# instanciate variables
current_state = StringVar()
processor = Processor()
# set initial state: normal, no effects
set_state('normal')
# start the processor
t = Thread(target=processor.run, daemon=True)
t.start()
if DEBUGGING: print('Creating widgets')
# everything will go intp a frame for layout
frame = Frame(app)
# defaults for all widgets and (layout-)grid in one place
grid_defaults = dict(padx=4, pady=5, ipadx=2, ipady=2, sticky=N+S+W+E, )
widgets_defaults = dict(background='#30536b', border=0, foreground='#00f7ff', )
# major buttons: record
Button(frame, text='Aufzeichnung start', command=record_start, **widgets_defaults) .grid(row=0, column=0, **grid_defaults)
Button(frame, text='Aufzeichnung stop', command=record_stop, **widgets_defaults) .grid(row=0, column=1, **grid_defaults) # TODO disable by flow
Button(frame, text='Zurück live', command=record_live, **widgets_defaults) .grid(row=0, column=2, **grid_defaults)
# reset to normal, no effects state
Button(frame, text='Normal', command=lambda: set_state('normal'), **widgets_defaults) .grid(row=1, column=0, **grid_defaults)
# here we start to add effects buttons, we get those from the processor, the only one knowing them
row, col = 1, 1,
for effect in processor.effects:
	if DEBUGGING: print('activating effect', effect)
	Button(frame, text=effect.capitalize(), command=Command(set_state, effect), **widgets_defaults) .grid(row=row, column=col, **grid_defaults)
	# we have a 3xn grid, so increase col as long as we arent at 3, then increase row
	col += 1
	if col >= 3:
		col = 0
		row += 1
# if we have a button in the current row jump to next row
if col:
	row += 1
# add the status label
Label(frame, textvariable=current_state, justify=LEFT, border=2,
	#relief=RIDGE, background='#2654de', foreground='#fff',
	).grid(row=row, columnspan=3, **grid_defaults)
# kick off layouting - tk will do for us just fine
frame.pack(expand=1, fill=BOTH)
# start the tk loop
app.mainloop()

