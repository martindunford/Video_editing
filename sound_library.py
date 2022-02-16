#! /usr/local/bin/python3

from setup_logger import *
import librosa
import sox
import numpy

# Sox notes
# Record audio: record martin1.wav (Ctrl-C exit)
# Play audio:   play martin1.wav trim 5.4  (plays starting at 5.3)
# Audio stats:  soxi martin1.wav
# Spectogram:   sox martin1.wav -n spectogram -o martin1.png

def find_peak(audio_file):
    sample_rate = sox.file_info.sample_rate (audio_file)
    logger.info (f'Sample rate: {sample_rate}')
    signal, _ = librosa.load(audio_file,sr=int(sample_rate))
    # print (numpy.ndarray.max(signal))

    peak = None
    maxval = max(signal)
    for ndx in range (0,len(signal)):
        if signal[ndx] >= maxval:
            # print (f'{ndx}: {signal[ndx]}')
            peak = round(ndx/sample_rate,4)
            return peak,sample_rate
    return 0.0,sample_rate


def main():
    peak = find_peak('martin1.wav')

    logger.info (f'Peak is at approx {peak} seconds')

if __name__ == '__main__':
    main()


