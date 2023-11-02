#! .venv/bin/python3

import subprocess
import shlex

from pprint import pprint
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

import tempfile
from jinja2 import Template
from subprocess import *
from iterfzf import *

from urllib.parse import quote
from setup_logger import *

import os,sys
import glob
from iterfzf import *
import ffmpeg

# Import everything needed to edit video clips
from moviepy.editor import *
from moviepy.video.fx.all import *
from moviepy.video.tools.drawing import circle

tasks = [
    f'{target} Get Clip size',
    f'{target} Crop Clip down to (x1,y1) to (x2,y2)',
    f'{target} Extract segment of Clip (any .mov or .mp4 in current directory tree) into another clip',
    f'{target} Speed up or slow down a Video Clip',
    Separator(),
    f'{target} Combine many clips',
    f'{target} Stack two clips',
    f'{target} Composite clip',
    Separator(),
    f'{green_book} Moviepy Effects Documentation',
    Separator(),
    f'{cactus} Work In Progress',
    Choice(value=None, name="Exit"),
]

# =====================================================================

def simple_motion(t):
    return 100+t*50,100+t*50,
def video_commander ():
    os.system ('clear')
    print ('')
    print ('')
    task = inquirer.select(
        message="Select action:",
        choices=tasks,
        height='100%',
        default=None,
    ).execute()
    if not task: return

    if 'Get Clip size' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        clip1 = VideoFileClip(input_file)
        logger.info (clip1.size)

    elif  'Crop Clip down to' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        clip1 = VideoFileClip(input_file)
        top_left = input ('Co-ordinates for top left (x,y)?:')
        bottom_right = input('Co-ordinates for bottom right (x,y)?:')
        x1,y1 = top_left.split(',')
        x2,y2 = bottom_right.split(',')
        clip1_cropped = crop(clip1, x1,y1,x2,y2)

        clip1_cropped.write_videofile(output_file, audio_codec="aac")


    elif 'Extract segment of Clip' in task:
        start = float(input ('Start point (seconds) of new clip?:'))
        end  = float(input ('End point (seconds) of new clip?:'))

        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        start_time = f'00:00:{start:02}'  # Start time for trimming (HH:MM:SS)
        end_time = f'00:00:{end:02}'  # End time for trimming (HH:MM:SS)

        logger.info (f'Creating new clip (extracting from {start_time} to {end_time}) in: {output_file}')
        ffmpeg.input(input_file, ss=start_time, to=end_time).output(output_file).run()

    elif 'Speed up or slow down a Video Clip' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        # Loading video dsa gfg intro video
        clip1  = VideoFileClip(input_file)
        sped_up_video = clip1.speedx(factor=2)
        # Codec needed or no audio !!
        sped_up_video.write_videofile(output_file,audio_codec="aac")

    elif 'Stack two clips' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        file1, file2 = iterfzf(vchoices, multi=True)
        clip1 = VideoFileClip(file1)
        clip2 = VideoFileClip(file2)
        output_file = f'Stacked_1.mp4'
        cinfo = [[clip1], [clip2]]
        final_clip = clips_array(cinfo)
        final_clip.write_videofile(output_file, audio_codec="aac")

    elif 'Composite clip' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        # file1, file2 = iterfzf(vchoices, multi=True)
        file1 = 'Video_clips/camp_footage.mov_1.mp4'
        file2 = 'Video_clips/commentary.mp4'
        clip1 = VideoFileClip(file1)
        clip2 = VideoFileClip(file2)

        clip2_small = clip2.resize(0.25)
        clip3 = VideoFileClip('Video_clips/the_finger.mp4')
        # clip3.set_position (simple_motion)
        clip3_small = clip3.resize(0.16)
        clip3_silent = clip3_small.without_audio()
        output_file = f'Stacked_1.mp4'
        video = CompositeVideoClip([clip1,
                                    clip2_small.set_position((1000, 100)),
                                    clip3_silent.set_position((50, 700))]
                                   )
        video.write_videofile(output_file, audio_codec="aac")

    elif 'Combine many clips' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        files = iterfzf(vchoices, multi=True)
        clips = [VideoFileClip(x) for x in files]
        output_file = f'Combined_1.mp4'
        final_clip = concatenate_videoclips(clips)
        ayes = input('Retain Audio (also sped up)?"')
        if ayes == 'y':
            final_clip.write_videofile(output_file, audio_codec="aac")
        else:
            final_clip.write_videofile(output_file)

    elif 'Moviepy Effects Documentation' in task:
        os.system (f'open https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.crop.html')

    elif 'Work In Progress' in task:
        # Rendered video from AE with RGB+Alpha
        mask = VideoFileClip("blueBox.mov", has_mask=True).mask
        video1 = TextClip("Hello world", fontsize=100, color="red", font="EndzoneTechCond-Bold.otf")
        # Created blank video for the background layer
        video2 = VideoFileClip("blackBox.mov")
        # Place the video1 on top of video2 while also applying the mask to video1.
        final_video = CompositeVideoClip([video2, video1.set_mask(mask)])
        # you could remove the audio information but I just copied this from an older file so I left it on
        final_video.set_duration(10).write_videofile("maskingTest.mp4", fps=30, codec='mpeg4', bitrate="4000k",
                                                     audio_codec="mp3")
        return
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        clip = VideoFileClip(input_file, audio=False).add_mask()
        w, h = clip.size
        logger.info (f'Clip dimensions are Height:{h}, Width:{w}')

        # The mask is a circle with vanishing radius r(t) = 800-100*t
        clip.mask.get_frame = lambda t: circle(screensize=(clip.w, clip.h),
                                               center=(clip.w/2, clip.h/4),
                                               radius=max(0, int(800 - 50*t)),
                                               col1=1, col2=0, blur=4)

        the_end = TextClip("The End", font="Amiri-bold", color="white",
                           fontsize=70).set_duration(clip.duration)

        final = CompositeVideoClip([the_end.set_pos('center'), clip],
                                   size=clip.size)

        final.write_videofile(output_file)



    else:
        logger.error (f'No matchng actions found for task: {task}')




if __name__ == '__main__':
    video_commander()