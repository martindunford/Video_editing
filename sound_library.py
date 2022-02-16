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

def find_peak(audio_file,look_in_initial_period=10):
    sample_rate = sox.file_info.sample_rate (audio_file)
    logger.info (f'Sample rate: {sample_rate}')
    signal, _ = librosa.load(audio_file,sr=int(sample_rate))
    # print (numpy.ndarray.max(signal))

    peak = None
    search_initial_samples = look_in_initial_period*int(sample_rate)
    maxval = max(signal[:search_initial_samples])

    # Looks for peak amplitude in initial smaples e.g a  hand clap before starting to play music  !!
    # otherwise part of recording might exceed it !!
    for ndx in range (0,search_initial_samples):
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



