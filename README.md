# Video Editing Application overview 
Replace and add audio tracks of videos and add text overlays etc

## Required module notes
To install pyaudio:

- `brew install portaudio`
- `python3 -m pip install pyaudio`

## Video editing in general
### Getting section of a video
This will extract first 20s of Rolling.mov into test1.mov
 ` ffmpeg -ss 0 -to 20 -i Rolling.mov test1.mov`

## Audio editing

### To install sox
`python3 -m pip install sox`

### Sox command line tool
- Record audio:` record martin1.wav` (Ctrl-C exit)
- Play audio:   `play martin1.wav trim 5.3`  (plays starting at 5.3)
- Audio stats:  `soxi martin1.wav`
- Spectogram:   `sox martin1.wav -n spectrogram -o martin1.png`
- Trim audio:  `sox htw.wav htw1.wav trim 0 45` (First 45 seconds extracted to htw1.wav)

## Image editing

`sips -x 1280 1080 Charlize.jpg `

Existing size: Ctrl click on image file name in Finder and is in the info section