#! /usr/local/bin/python3

# Import everything needed to edit video clips
from moviepy.editor import *
from PIL import Image

from setup_logger import *
from sound_library import *
import tempfile
import time
import os.path
import argparse


class Viktor:
    ''' Viktor the video manipulator
    '''
    # --------------------
    def __init__ (self,video_file):
        self.video_file = video_file
        self.complete_clip = VideoFileClip(self.video_file)
        logger.info (f'Original Clip size is: {self.complete_clip.size}')
        self.original_audio = self.complete_clip.audio
        self.all_video_clips = [self.complete_clip]
        self.video = CompositeVideoClip(self.all_video_clips)

    # --------------------
    def find_peak_audio_amplitude(self):
        tf = tempfile.NamedTemporaryFile(suffix='.wav')
        self.info (f'Extracting audio track for Movie {self.video_file} into {tf.name}')
        self.complete_clip.audio.write_audiofile(tf.name)

        self.peak_audio,self.sample_rate = find_peak (tf.name)
        self.info (f'Found audio peak for {self.video_file} at: {self.peak_audio} seconds')

        return self.peak_audio, self.sample_rate

    # --------------------
    def add_audio_track (self, audio_file, insert_at, replace_original_audio=True):
        if not self.sample_rate:
            self.find_peak_audio_amplitude()

        insert_file_peak_audio,_ = find_peak(audio_file)
        self.info (f'Found audio peak for {audio_file} at: {insert_file_peak_audio} seconds')
        insert_at = self.peak_audio - insert_file_peak_audio

        if replace_original_audio:
            self.info (f'Replacing audio (for {self.video_file}) starting at: {insert_at} seconds with audio from {audio_file}')
        else:
            self.info (f'Adding additional audio track ({audio_file}) to video {self.video_file}')
        audioclip1 = AudioFileClip(audio_file,fps=self.sample_rate)
        # audioclip1.preview()

        if replace_original_audio:
            all_audio_clips = [
                audioclip1.set_start(insert_at)
            ]
        else:
            all_audio_clips = [
                self.original_audio,
                audioclip1.set_start(insert_at)
            ]
        # To add audio only way seems to be to assign a CompositeAudioClip
        #  to clip.audio.
        new_audioclip = CompositeAudioClip(all_audio_clips)
        self.complete_clip.audio = new_audioclip

        # Reduce the audio volume (volume x 1.8)
        # clip = clip.volumex(1.2)

    # --------------------
    def add_text_overlay (self, mytext, insert_at, duration, font_size=70, mycolor='white',position='center'):
        # Animation, See: https://towardsdatascience.com/rendering-text-on-video-using-python-1c006519c0aa
        self.info (f'Adding text overlay at {insert_at} secs to be displayed for: {duration} secs ')
        # Generate a text clip. You can customize the font, color, etc.
        txt_clip = TextClip(mytext,fontsize=font_size,color=mycolor)

        # Say that you want it to appear 10s at the center of the screen
        txt_clip = txt_clip.set_pos(position).set_duration(duration)

        # Overlay the text clip on the first video clip
        self.all_video_clips.append (txt_clip.set_start(insert_at))
        self.video = CompositeVideoClip(self.all_video_clips)

    # ----------------------
    # https://github.com/Zulko/moviepy/issues/964 (Am using this)
    # https://www.geeksforgeeks.org/replace-green-screen-using-opencv-python/

    def replace_green_screen_with_bkg_image(self,bkgimage_file):
        self.info (f'Replacing Green Screen with: {bkgimage_file}')
        background = ImageClip (bkgimage_file)
        masked_clip = self.complete_clip.fx(vfx.mask_color, color=[0, 206, 128], thr=120, s=5)
        self.all_video_clips.remove (self.complete_clip)
        self.all_video_clips.append (background)
        self.all_video_clips.append (masked_clip)

    def replace_green_screen_with_bkg_video(self,bkgvideo_file):
        self.info (f'Replacing Green Screen with: {bkgvideo_file}')
        background = VideoFileClip (bkgvideo_file)
        background.set_position ((0,0))
        logger.info (f'Background video size: {background.size}')
        masked_clip = self.complete_clip.fx(vfx.mask_color, color=[0, 206, 128], thr=120, s=5)
        self.all_video_clips.remove (self.complete_clip)
        self.all_video_clips.append (background)
        self.all_video_clips.append (masked_clip)

    # --------------------
    def render_video_to (self, output_file):
        self.info (f'Rendering to: temp.mp4')
        # Write the result to a file (many options available !)
        self.video.write_videofile(
            'temp.mp4',
            audio_codec='aac' # Should not be needed but there is bug.
        )

        # For iPhone video with size 1920x1080 following needed to get correct aspect ratio
        self.info (f'Ensuring Aspect Ratio correct (writing to {output_file}')
        os.system (f'ffmpeg -i temp.mp4 -c copy -aspect 9:16 {output_file}')

    # --------------------
    def trim_video (self,start_time,end_time,ofile_name):
        self.info (f'Extracting {start_time}:{end_time} from {self.video_file} into {ofile_name}')
        tcmd = f'ffmpeg -ss {start_time} -to {end_time} -i {self.video_file} -c copy {ofile_name}'
        os.system (tcmd)

    # --------------------
    def trim_audio (self,start_time,end_time,audio_file, ofile_name):
        self.info (f'Extracting {start_time}:{end_time} from {audio_file} into {ofile_name}')
        tcmd = f'sox  {audio_file}  {ofile_name} trim {start_time} {end_time} '
        os.system (tcmd)
    # --------------------
    def info(self, msg):
        logger.info(f'{self.__class__.__name__}: {msg}')

import cv2
import numpy as np

def replace_green():
    ofile = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280,1080))
    video = cv2.VideoCapture("Rolling.mov")
    image = cv2.imread("Burren-Limestone.jpg")
    image = cv2.resize (image,(1280, 1080))

    while True:
        ret, frame = video.read()

        if ret:
            frame = cv2.resize(frame, (1280, 1080))

            # OpenCV usually captures images and videos in 8-bit, unsigned integer, BGR forma
            u_green = np.array([200, 248, 80])
            l_green = np.array([30, 50, 0])

            mask = cv2.inRange(frame, l_green, u_green)
            # mask = create_mask_with_threshold(frame)
            res = cv2.bitwise_and(frame, frame, mask = mask)

            f = frame - res
            f = np.where(f == 0, image, f)
            # cv2.imshow("video", frame)
            # cv2.imshow("mask", f)

            ofile.write(f)

            # Press Q on keyboard to stop processing
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Last frame read
            break

    video.release()
    cv2.destroyAllWindows()

def create_mask_with_threshold(frame):
    # split the the B, G and R channels
    b, g, r = cv2.split(frame)

    # create the threshold
    _, mask = cv2.threshold(g, 200, 50, cv2.THRESH_BINARY_INV)

    # De-noise the threshold to get a cleaner mask
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))

    return mask


def replace_background(frame, bg, mask):
    # if the pixel on threshold is background then make it white
    frame[mask == 0] = 255

    # if the pixel on threshold is not background then make it black
    bg[mask != 0] = 255

    # combine both images into frame
    return cv2.bitwise_and(bg, frame)

def wip1():
    replace_green()

def wip2():
    image = cv2.imread("Burren-Limestone.jpg")

    image = cv2.resize(image, (1280, 1080))
    cv2.imshow("video", image)

    while 1:
        if cv2.waitKey(25) == 27:
            break

def wip3():
    video = cv2.VideoCapture("Rolling.mov")
    image = cv2.imread("Burren-Limestone.jpg")

    ret, frame = video.read()

    frame = cv2.resize(frame, (1280, 1080))
    image = cv2.resize(image, (1280, 1080))


    # OpenCV usually captures images and videos in 8-bit, unsigned integer, BGR forma
    u_green = np.array([200, 248, 70])
    l_green = np.array([30, 70, 0])

    mask = cv2.inRange(frame, l_green, u_green)
    # mask = create_mask_with_threshold(frame)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    f = frame - res
    f = np.where(f == 0, image, f)

    cv2.imshow("video", frame)
    cv2.imshow("mask", f)

    while 1:
        if cv2.waitKey(25) == 27:
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('-b', '--bimage',
                        help='Replace green screen with an image')
    parser.add_argument('-c', '--bvideo',
                        help='Replace green screen with a video')
    parser.add_argument('-a', '--audio',
                        help='Replacement audio track (Note: both video and audio need an initial loud sync sound (e.g handclap_')
    parser.add_argument('-v', '--video',
                        help='Video file to be altered')
    parser.add_argument('-t', '--trim',
                        help='Only produce the first N seconds of video (save time to see if what was intended works!) ')
    args = parser.parse_args()

    video_file = args.video
    vik = Viktor(video_file)
    outputfile = f'{os.path.basename(video_file).split(".")[0]}.mp4'

    os.system ('rm trim.*')
    if args.trim:
        vik.trim_video (0,args.trim,'trim.mov')
        vik = Viktor ('trim.mov')

    # Tested and work
    # bkg_image = 'Burren-Limestone.jpg'
    # bkg_image = 'bad_moon1_resized.png'
    # bkg_video = 'wild_weather.mov'

    os.system(f'rm -f {outputfile} temp.mp4')

    # ________________________
    if args.audio:
        audiofile = args.audio
        if args.trim:
            vik.trim_audio (0,args.trim,audiofile,'trim.wav')
            audiofile = 'trim.wav'

        peak_audio_point,_ = vik.find_peak_audio_amplitude ()
        vik.add_audio_track (audiofile,peak_audio_point)

    # TODO:
    # vik.add_text_overlay('Rolling - JJ Cale',2,20, position='top')
    # vik.add_text_overlay('Recorded Feb 17, 22 using Tascam 12!',2,10, font_size=30,mycolor='yellow')

    if args.bimage:
        vik.replace_green_screen_with_bkg_image(args.bimage)
    if args.bvideo:
        vik.replace_green_screen_with_bkg_video(args.bvideo)
    vik.render_video_to(outputfile)


def resize_image (image, new_size):
    '''
    Resize and image
    :param image: Name of image file
    :param new_size: A tuple (width, height)
    :return: 
    '''
    b_image = Image.open(image)
    logger.info (f'Background image has size: {b_image.height} x {b_image.width}')
    b_image = b_image.resize(new_size)


    b_image.save (f'{image.split(".")[0]}_resized.png')

if __name__ == '__main__':
    main()
    # resize_image ('bad_moon1.png',(1280,1920))
