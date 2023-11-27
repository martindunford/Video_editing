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
import numpy as np
from PIL import Image
# importing necessary packages
import cv2

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
    f'{target} Blend/Merge two videos using specified weighting of background video',
    Separator(),
    f'{target} Replace color in image with another color (RGB values needed!!)',
    f'{target} Resize an image',
    Separator(),
    f'{green_book} Moviepy Effects Documentation',
    f'{sun} Demo of blending a logo onto an image (basis of masking and blending)',
    Separator(),
    f'{cactus} Work In Progress',
    f'{cactus} Another Work In Progress',
    Choice(value=None, name="Exit"),
]

# =====================================================================

def simple_motion(t):
    return 1000-t*100,700-t*70

originx = 1000
originy = 200
radius = 200
from math import *
def circular_motion1 (t):
    angle = t*2
    return originx + cos(angle)*radius,originy + sin(angle)*radius;

radius = 40
def circular_motion (t):
    angle = t*4
    return originx -t*70,originy + sin(angle)*radius;
def evasive_action(t):
    if t>7:
        return 100,100+(t-7)*50
    else:
        return 100,100

def blend_videos(video1_path, video2_path, output_path, alpha=0.5,display_frames=False):
    # Open video files
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    # Get video properties
    width = int(cap1.get(3))
    height = int(cap1.get(4))
    fps = int(cap1.get(5))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # Break the loop if either video is finished
        if not ret1 or not ret2:
            break

        # Blend frames using alpha parameter
        blended_frame = cv2.addWeighted(frame1, alpha, frame2, 1 - alpha, 0)

        # Write the blended frame to the output video
        out.write(np.uint8(blended_frame))

        if display_frames:
            # Display the result (optional)
            cv2.imshow('Blended Video', blended_frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    # Release video capture and writer objects
    cap1.release()
    cap2.release()
    out.release()

    # Close OpenCV windows (optional)
    cv2.destroyAllWindows()
    logger.info (f'Blended video ready in: {output_path}')

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
        output_file = f'{input_file.split(".")[0]}_1.mp4'

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
        file2 = 'Video_clips/commentary1.mov'
        clip1 = VideoFileClip(file1)
        logger.info (clip1.size)

        clip2 = VideoFileClip(file2)
        # The first resize needed if it came from iphone (not sure why!)
        clip2_final = clip2.resize((clip2.h, clip2.w)).resize(0.16)
        logger.info (clip2.size)

        clip3 = VideoFileClip('Video_clips/the_finger.mp4')
        clip3_final = clip3.resize(0.16).without_audio()

        output_file = f'Stacked_1.mp4'
        video = CompositeVideoClip([clip1,
                                    clip2_final.set_position(evasive_action),
                                    clip3_final.set_position(circular_motion)],
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

    elif 'Blend/Merge two videos using' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        fg_path,bg_path = iterfzf(vchoices, multi=True)
        weighting = float (input (f'Merge {fg_path} and {bg_path}, weighting for background {bg_path}?:'))
        display_frames = input (f'Display merged video frame by frame as it is being produced?:') or False
        if display_frames:
            display_frames = True
        blend_videos(fg_path, bg_path, 'martin_blended.mp4', alpha=weighting,display_frames=display_frames)

    elif '1 Work In Progress' in task:
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        clip = VideoFileClip(input_file, audio=False).add_mask()

        # 2. Create a mask that is black everywhere except for a white circle in the center
        def make_circle_mask(size):
            Y, X = np.ogrid[:size, :size]
            center = size / 2
            distance_from_center = np.sqrt((X - center) ** 2 + (Y - center) ** 2)
            mask = 255 * (distance_from_center <= size / 2)
            return mask.astype(np.uint8)

        circle_mask = ImageClip(make_circle_mask(60), ismask=True)

        # 3. Apply the mask to the ColorClip to get a round bubble
        clip = clip.set_mask(circle_mask)
        clip.write_videofile(output_file)
        return
        # # Rendered video from AE with RGB+Alpha
        # mask = VideoFileClip("blueBox.mov", has_mask=True).mask
        # video1 = TextClip("Hello world", fontsize=100, color="red", font="EndzoneTechCond-Bold.otf")
        # # Created blank video for the background layer
        # video2 = VideoFileClip("blackBox.mov")
        # # Place the video1 on top of video2 while also applying the mask to video1.
        # final_video = CompositeVideoClip([video2, video1.set_mask(mask)])
        # # you could remove the audio information but I just copied this from an older file so I left it on
        # final_video.set_duration(10).write_videofile("maskingTest.mp4", fps=30, codec='mpeg4', bitrate="4000k",
        #                                              audio_codec="mp3")
        # return
        vchoices = glob.glob('**/*.mov') + glob.glob('**/*.mp4')
        input_file =  iterfzf(vchoices,multi=False)
        output_file = f'{os.path.basename(input_file)}_1.mp4'

        clip = VideoFileClip(input_file, audio=False).add_mask()
        w, h = clip.size
        logger.info (f'Clip dimensions are Height:{h}, Width:{w}')

        # The mask is a circle with vanishing radius r(t) = 800-100*t
        clip.mask.get_frame = lambda t: circle(screensize=(clip.w, clip.h),
                                               center=(clip.w/2, clip.h/4),
                                               # radius=max(0, int(800 - 50*t)),
                                               radius=100,
                                               col1=1, col2=0, blur=4)

        the_end = TextClip("The End", font="Amiri-bold", color="white",
                           fontsize=70).set_duration(clip.duration)

        final = CompositeVideoClip([the_end.set_pos('center'), clip],
                                   size=clip.size)

        final.write_videofile(output_file)

    elif 'Replace color in image with another color' in task:
        ichoices = glob.glob('*.png') + glob.glob('*.jpg')
        img_name = iterfzf (ichoices,multi=False)
        f1,f2 = os.path.split(img_name)
        img_out_name = os.path.join(f1,f'{f2.split(".")[0]}_new.png')
        # color1 = input ('Color to replace (RGB e.g 100,222,1 )?:')
        # color2 = input ('Replacement color (RGB e.g 100,222,1)?:')

        im = Image.open(img_name)
        data = np.array(im)

        # r1, g1, b1 = color1.split(',')
        # r2, g2, b2 = color2.split(',')
        r1, g1, b1 = 255,255,254
        r2, g2, b2 = 97,83,70

        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask1 = (red == r1) & (green == g1) & (blue == b1)
        mask2 = (red == r2) & (green == g2) & (blue == b2)
        data[:, :, :3][mask1] = [r2, g2, b2]
        data[:, :, :3][mask2] = [r1, g1, b1]

        im = Image.fromarray(data)
        logger.info (f'Color has been replaced in: {img_out_name}')
        im.save(img_out_name)

    elif 'Resize an image' in task:
        ichoices = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.webp')
        img_name = iterfzf (ichoices,multi=False)
        f1,f2 = os.path.split(img_name)
        img_out_name = os.path.join(f1,f'{f2.split(".")[0]}_new.png')

        im1 = Image.open(img_name)
        logger.info (f'Image size: {im1.size}')

        newsize = input ('New size?:')
        fields = newsize.split(',')
        newsize = (int(fields[0]),int(fields[1]))
        im1 = im1.resize(newsize)

        logger.info (f'Resized image in: {img_out_name}')
        im1.save(img_out_name)

    elif 'Another Work In Progress' in task:
        # ChatGPT wrote this for me!
        # White Circle moving diagonally across a black background
        width, height = 1920,1080
        fps = 30
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vname = 'moving_circle_video.mp4'
        out = cv2.VideoWriter(vname, fourcc, fps, (width, height))

        # Set circle properties
        circle_radius = 200
        circle_color = (255, 255, 255)  # White

        # Initialize video frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Main loop to create frames for the video
        for t in range(0, width + height):
            # Calculate circle position based on time
            x = min(width - 1, t)
            y = min(height - 1, t)

            # Create a new frame with a black background
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Draw a white circle on the frame
            cv2.circle(frame, (x, y), circle_radius, circle_color, -1)

            # Write the frame to the video
            out.write(frame)

        # Release the VideoWriter
        out.release()
        logger.info (f'Video ready in {vname}')
    elif 'Demo of blending a logo onto' in task:
        # Load two images
        img1 = cv2.imread('blending/messi.jpg')
        img2 = cv2.imread('blending/cv.png')
        # assert img1 is not None, "file could not be read, check with os.path.exists()"
        assert img2 is not None, "file could not be read, check with os.path.exists()"
        # I want to put logo on top-left corner, So I create a ROI
        rows, cols, channels = img2.shape
        # Top left portion of image1 that is size of image2
        roi = img1[0:rows, 0:cols]
        # Now create a mask of logo and create its inverse mask also
        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Step 1', img2gray)
        cv2.waitKey(0)
        # Threshold is 10. So almost everything converted to 255 (white)
        #  then inverted so white on black to black on white
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        cv2.imshow('Step 2', mask_inv)
        cv2.waitKey(0)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        cv2.imshow('Step 3', img1_bg)
        cv2.waitKey(0)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
        cv2.imshow('Step 4', img2_fg)
        cv2.waitKey(0)

        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg, img2_fg)
        img1[0:rows, 0:cols] = dst
        cv2.imshow('Step 5', img1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        logger.error (f'No matchng actions found for task: {task}')




if __name__ == '__main__':
    video_commander()