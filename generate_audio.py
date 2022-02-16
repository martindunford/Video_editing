#! /usr/local/bin/python3

import math
from pyaudio import PyAudio, paUInt8
import wave
from setup_logger import *

# import numpy
# from scipy.io.wavfile import write

# Notes
#
# To install pyaudio
# - brew install portaudio
# - python3 -m pip install pyaudio

def generate_sine_wave(frequency, duration, volume=0.2, sample_rate=22050):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''
    if sample_rate < (frequency * 2):
        print('Warning: sample_rate must be at least double the frequency '
              f'to accurately represent it:\n    sample_rate {sample_rate}'
              f' ≯ {frequency*2} (frequency {frequency}*2)')

    num_samples = int(sample_rate * duration)
    rest_frames = num_samples % sample_rate

    pa = PyAudio()
    stream = pa.open(
        format=paUInt8,
        channels=1,  # mono
        rate=sample_rate,
        output=True,
    )

    # make samples
    s = lambda i: volume * math.sin(2 * math.pi * frequency * i / sample_rate)
    # TODO: Must be way to reuse the samples generator here?
    samples = (int(s(i) * 0x7F + 0x80) for i in range(num_samples)) # samples is a  generator
    samples1 = (int(s(i) * 0x7F + 0x80) for i in range(num_samples)) # samples is a  generator
    lsamples = [] # lsamples is a list

    # write several samples at a time
    for buf in zip( *([samples] * sample_rate) ):
        stream.write(bytes(buf))

    for buf in zip( *([samples1] * sample_rate) ):
        lsamples.append(bytes(buf))

    # # fill remainder of frameset with silence
    logger.info ('Silence')
    stream.write(b'\x80' * rest_frames)

    stream.stop_stream()
    stream.close()
    pa.terminate()


    # https://stackoverflow.com/questions/66979769/python-how-to-convert-pyaudio-bytes-into-virtual-file
    # save the recorded data as wav file using python `wave` module
    logger.info (f'There are {len(lsamples)} samples ')

    wf = wave.open('generated_tone.wav','wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(paUInt8))
    wf.setframerate(48000)
    wf.writeframes(b''.join(lsamples))
    wf.close()

def main():
    generate_sine_wave(
        # see http://www.phy.mtu.edu/~suits/notefreqs.html
        frequency=523.25,   # Hz, waves per second C6
        duration=1.5,       # seconds to play sound
        volume=0.25,        # 0..1 how loud it is
        sample_rate=48000,  # number of samples per second: 11025, 22050, 44100
    )

if __name__ == '__main__':
    main()