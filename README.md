# Video Editing
Replace and add audio tracks of videos and add text overlays etc

## Module notes
To install pyaudio:

- `brew install portaudio`
- `python3 -m pip install pyaudio`

To install sox 

`python3 -m pip install sox`

## Sox command line tool
- Record audio:` record martin1.wav` (Ctrl-C exit)
- Play audio:   `play martin1.wav trim 5.3`  (plays starting at 5.3)
- Audio stats:  `soxi martin1.wav`
- Spectogram:   `sox martin1.wav -n spectogram -o martin1.png`


