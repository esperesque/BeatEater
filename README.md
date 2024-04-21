# BeatEater
## Authors: Jakob Karlstrand, Hassan Mustafa and Levi Tuoremaa

A simple PyGame rhythm game that generates levels from user-selected audio tracks. Initially developed for the Physics of Sound class at Linköping University.

!["Brief gameplay footage"](demo_gif.gif)

Dependencies:
-PyGame
-Aubio
-SciPy
-PyDub

To start the game, run the file gameLoop.py. The player is controlled with the left and right arrow keys.

The program loads a user-specified music track as a .wav file and splits it into a bass, mid and treble track. Amplitude peaks in each track will produce falling notes in sync with the music on the left, middle and right side of the playing field respectively.

The track included with the project is Megaboss by Aaron Krogh.
