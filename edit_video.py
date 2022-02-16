#! /usr/local/bin/python3

# Import everything needed to edit video clips
from moviepy.editor import *
from setup_logger import *
from sound_library import *
import tempfile

def main():
    video_file = 'htonk.mov'
    add_audio = 'htonk.wav'
    # Load video
    clip = VideoFileClip(video_file)

    tf = tempfile.NamedTemporaryFile(suffix='.wav')
    logger.info (f'Extracting audio track for Movie {video_file} into {tf.name}')
    clip.audio.write_audiofile(tf.name)

    peak_audio,sample_rate = find_peak (tf.name)
    logger.info (f'Found audio peak at {peak_audio}')

    audioclip1 = AudioFileClip(add_audio,fps=sample_rate)
    # Plays the audip
    # audioclip1.preview()

    # To add audio only way seems to be to assign a CompositeAudioClip
    #  to clip.audio.
    # So original track has to be explicitly part of that !! i.e clip.audio
    # new_audioclip = CompositeAudioClip([audioclip1.set_start(peak_audio),clip.audio])
    new_audioclip = CompositeAudioClip([audioclip1.set_start(peak_audio)])

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