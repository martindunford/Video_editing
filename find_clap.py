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

def main():
    file = 'martin1.wav'
    sample_rate = sox.file_info.sample_rate (file)
    logger.info (f'Sample rate: {sample_rate}')
    signal, _ = librosa.load(file,sr=int(sample_rate))
    # print (numpy.ndarray.max(signal))

    for ndx in range (0,len(signal)):
        if signal[ndx] >= 1.0:
            # print (f'{ndx}: {signal[ndx]}')
            logger.info (f'Peak is at approx {round(ndx/sample_rate,4)} seconds')
            break


if __name__ == '__main__':
    main()



