#! /Users/martin/VENVS/py3.11/bin/python3
# -*- coding: utf-8 -*-
"""
list prompt example
"""
# from __future__ import print_function, unicode_literals

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


tasks = [
    f'{target} Extract segment of Clip (any .mov or .mp4 in current directory tree) into another clip',
    f'{target} Speed up or slow down a Video Clip',
    f'{target} Combine many clips',
    f'{target} Stack two clips',
    f'{target} Composite clip',

    Separator(),
    Choice(value=None, name="Exit"),
]

# =====================================================================
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


    if 'Extract segment of Clip' in task:
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
        file2 = 'Video_clips/commentary.mov_1.mp4'
        clip1 = VideoFileClip(file1)
        clip2 = VideoFileClip(file2)

        clip2_small = clip2.resize(0.25)
        clip3 = VideoFileClip('Video_clips/the_finger.mp4')
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




if __name__ == '__main__':
    video_commander()