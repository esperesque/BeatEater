from scipy.io import wavfile
from scipy import signal
import numpy

from pydub import AudioSegment

def bandSplit(path):
    monoFile = AudioSegment.from_wav(path)
    monoFile = monoFile.set_channels(1)
    monoFile.export("mono_file.wav", format="wav")

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=250, fs=sr, pass_zero="lowpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_bass.wav", sr, x.astype(numpy.int16))

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=[250, 4000], fs=sr, pass_zero="bandpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_mid.wav", sr, x.astype(numpy.int16))

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=4000, fs=sr, pass_zero="highpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_treb.wav", sr, x.astype(numpy.int16))
