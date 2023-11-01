# Video Editing Application overview 
Replace and add audio tracks of videos and add text overlays etc

Note that using VENY python3.11 from now on (after Version_1.0 (git tag))
and that an intuitive **video_commander.py** Application is the first stop
to easily get the results you desire

## Required module notes
To install pyaudio:

- `brew install portaudio`
- `python3 -m pip install pyaudio`

## Video editing in general
### Getting section of a video
This will extract first 20s of Rolling.mov into test1.mov

 ` ffmpeg -ss 0 -to 20 -i Rolling.mov -c copy test1.mov`

Combine several videos into one 

`ls video1.mp4 video2.mp4 | while read line; do echo file \'$line\'; done | ffmpeg -protocol_whitelist file,pipe -f concat -i - -c copy output.mp4
`

To find the dimensions of video 

`ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 bad_moon.mov`

`1920x1080`

### Green screen stock! (Cool)
https://greenscreenstock.com/video-footage/military/

https://www.shutterstock.com/video/search/green+screen?kw=green%20screen%20stock%20footage&c3apidt=p15784502820&gclid=CjwKCAiA6seQBhAfEiwAvPqu19dU6bmicD54ddUrGnqys44S5Hi710S8jeFxZ1XS0q_0kJSWUUPtLBoC3AQQAvD_BwE&gclsrc=aw.ds

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
or

`sips -g pixelWidth -g pixelHeight bad_moon.jpg`

So get a background image. 
Crop and extract a region with movie aspect ratio, e.g 1920x1280 (1.84) for iPhone
Resize it (Python PIL module) to these dimensions (1920x1280)