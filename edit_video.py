#! /usr/local/bin/python3

# Import everything needed to edit video clips
from moviepy.editor import *
from setup_logger import *
from sound_library import *
import tempfile

class Viktor:
    ''' Viktor the video manipulator
    '''
    # --------------------
    def __init__ (self,video_file):
        self.video_file = video_file
        self.complete_clip = VideoFileClip(self.video_file)
        self.original_audio = self.complete_clip.audio
        self.all_video_clips = [self.complete_clip]

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
    def add_text_overlay (self, mytext, insert_at, duration, font_size=70, mycolor='white'):
        # Animation, See: https://towardsdatascience.com/rendering-text-on-video-using-python-1c006519c0aa
        self.info (f'Adding text overlay at {insert_at} secs to be displayed for: {duration} secs ')
        # Generate a text clip. You can customize the font, color, etc.
        txt_clip = TextClip(mytext,fontsize=font_size,color=mycolor)

        # Say that you want it to appear 10s at the center of the screen
        txt_clip = txt_clip.set_pos('center').set_duration(duration)

        # Overlay the text clip on the first video clip
        self.all_video_clips.append (txt_clip.set_start(insert_at))
        self.video = CompositeVideoClip(self.all_video_clips)

    # --------------------
    def render_video_to (self, output_file):
        self.info (f'Rendering to: {output_file}')
        # Write the result to a file (many options available !)
        self.video.write_videofile(
            output_file,
            audio_codec='aac' # Should not be needed but there is bug.
        )

    # --------------------
    def info(self, msg):
        logger.info(f'{self.__class__.__name__}: {msg}')

def main():
    video_file = 'htw.mov'

    vik = Viktor(video_file)
    peak_audio_point,sample_rate = vik.find_peak_audio_amplitude ()

    vik.add_audio_track ('htw.wav',peak_audio_point)
    vik.add_text_overlay('Recorded live in Kinvara',2,7)
    vik.add_text_overlay('Martin Dunford does the Rolling Stones!',10,20, font_size=30,mycolor='yellow')
    vik.render_video_to('spire.mp4')


if __name__ == '__main__':
    main()