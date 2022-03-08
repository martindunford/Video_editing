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
        self.duration = self.complete_clip.duration

        logger.info (f'Original Clip size is: {self.complete_clip.size}')
        self.original_size = self.complete_clip.size
        self.original_audio = self.complete_clip.audio
        self.all_video_clips = [self.complete_clip]
        self.video = CompositeVideoClip(self.all_video_clips)

        self.find_peak_audio_amplitude()

        # The output video to start 2 seconds after hand clap
        self.video.set_start(self.peak_audio+2)

    # --------------------
    def find_peak_audio_amplitude(self):
        if self.complete_clip.audio:
            tf = tempfile.NamedTemporaryFile(suffix='.wav')
            self.info (f'Extracting audio track for Movie {self.video_file} into {tf.name}')
            self.complete_clip.audio.write_audiofile(tf.name)

            self.peak_audio,self.sample_rate = find_peak (tf.name)
            self.info (f'Found audio peak for {self.video_file} at: {self.peak_audio} seconds')

            return self.peak_audio, self.sample_rate
        else:
            self.peak_audio, self.sample_rate = 0,48000
            return 0,48000 # No sound track

    # --------------------
    def add_audio_track (self, audio_file, insert_at, replace_original_audio=True):
        if self.peak_audio: # Video has an existing sound track
            insert_file_peak_audio,_ = find_peak(audio_file)
            self.info (f'Found audio peak for {audio_file} at: {insert_file_peak_audio} seconds')

            insert_at = round (self.peak_audio - insert_file_peak_audio,4)
        else:
            insert_at = 0

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
        # Note: Digital Color Meter app (OX-X) to get closest RGB for color of the green screen
        masked_clip = self.complete_clip.fx(vfx.mask_color, color=[0, 206, 128], thr=120, s=5)

        # We don't want the original clip just the new masked one and the backgrond video
        #  in the masked portion of same
        self.all_video_clips.remove (self.complete_clip)
        self.all_video_clips.append (background)
        # We only want video after the detected hand clap/sync sound !!
        self.all_video_clips.append (masked_clip.subclip(self.peak_audio+2,self.duration))

    def replace_green_screen_with_bkg_video(self,bkgvideo_file):
        self.info (f'Replacing Green Screen with: {bkgvideo_file}')
        background = VideoFileClip (bkgvideo_file)
        # background.set_position ((0,0))
        logger.info (f'Background video size: {background.size}')

        number_of_clips = max (1,self.video.duration//background.duration)
        self.info (f'Will need to concatenate background video {number_of_clips} times!')
        if number_of_clips > 1:
            clips = int(number_of_clips)*[background]
            background1 = concatenate_videoclips(clips,
                                                method="compose")
        else:
            background1 = background

        # Note: Digital Color Meter app (OX-X) to get closest RGB for color of the green screen
        masked_clip = self.complete_clip.fx(vfx.mask_color, color=[0, 246, 57], thr=170, s=5)

        # We don't want the original clip just the new masked one and the backgrond video
        #  in the masked portion of same
        self.all_video_clips.remove (self.complete_clip)
        self.all_video_clips.append (background1)
        # We only want video after the detected hand clap/sync sound !!
        self.all_video_clips.append (masked_clip)

    # --------------------
    def render_video_to (self, output_file, subclip=None):
        self.info (f'Rendering to: temp.mp4')
        # Write the result to a file (many options available !)

        if subclip:
            self.info (f'Extracting subclip from {subclip[0]} to {subclip[1]}')
            self.video = self.video.subclip(t_start=subclip[0],
                                            t_end=subclip[1])

        logger.info (f'Final size is: {self.video.size}')

        self.video.write_videofile(
            'temp.mp4',
            audio_codec='aac' # Should not be needed but there is bug.
        )

        if list(self.video.size) != list(self.original_size):
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


def wip1():
    video_file = 'temp1.mov'
    complete_clip = VideoFileClip(video_file)

    logger.info (f'Original Clip size is: {complete_clip.size}')
    all_video_clips = [complete_clip]
    video = CompositeVideoClip(all_video_clips)
    video1 = video.subclip(10,15)
    video1.write_videofile(
        'temp1.mp4',
        audio_codec='aac' # Should not be needed but there is bug.
    )

def wip2():
    video_file = 'wild_weather.mov'
    clip1 = VideoFileClip(video_file)
    newclip1 = concatenate_videoclips (2*[clip1])

    all_video_clips = [newclip1]
    video1 = CompositeVideoClip(all_video_clips)
    video1.write_videofile(
        'temp1.mp4',
        audio_codec='aac' # Should not be needed but there is bug.
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    parser.add_argument( '--clap', action='store_true',
                        help='Output video contains clap. Default is it starts 2 seconds after point of hand clap used to sync with audio')
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

    # Tested and work
    # bkg_image = 'Burren-Limestone.jpg'
    # bkg_image = 'bad_moon1_resized.png'
    # bkg_video = 'wild_weather.mov'

    os.system(f'rm -f {outputfile} temp.mp4')

    # ________________________
    if args.audio:
        audiofile = args.audio
        peak_audio_point,_ = vik.find_peak_audio_amplitude ()
        vik.add_audio_track (audiofile,peak_audio_point)

    # TODO:
    # vik.add_text_overlay('Rolling - JJ Cale',2,20, position='top')
    # vik.add_text_overlay('Recorded Feb 17, 22 using Tascam 12!',2,10, font_size=30,mycolor='yellow')

    if args.bimage:
        vik.replace_green_screen_with_bkg_image(args.bimage)
    elif args.bvideo:
        vik.replace_green_screen_with_bkg_video(args.bvideo)

    # From 2 seconds past hand clap to the end
    subclip=(vik.peak_audio+2,None)
    if args.clap:
        subclip = None
        logger.info (f'subclap = {subclip}')
    vik.render_video_to(outputfile,
                        subclip=subclip
                        )


if __name__ == '__main__':
    main()
    # resize_image ('bad_moon1.png',(1280,1920))
