#! /usr/local/bin/python3

# Import everything needed to edit video clips
from moviepy.editor import *
from setup_logger import *

def main():
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    clip = VideoFileClip("htonk.mov")

    audioclip1 = AudioFileClip("htonk.wav",fps=48000)
    # Plays the audip
    # audioclip1.preview()

    # To add audio only way seems to be to assign a CompositeAudioClip
    #  to clip.audio.
    # So original track has to be explicitly part of that !! i.e clip.audio
    new_audioclip = CompositeAudioClip([audioclip1,clip.audio])

    # Reduce the audio volume (volume x 1.8)
    # clip = clip.volumex(1.2)

    # Generate a text clip. You can customize the font, color, etc.
    txt_clip = TextClip("Rolling Stones",fontsize=70,color='white')

    # Say that you want it to appear 10s at the center of the screen
    txt_clip = txt_clip.set_pos('center').set_duration(10)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])
    # Audio added here? but why not above like Text is!! 
    video.audio = new_audioclip

    # Write the result to a file (many options available !)
    video.write_videofile("coolio.mp4",
                          audio_codec='aac' # Should not be needed but there is bug.
                          )

if __name__ == '__main__':
    main()