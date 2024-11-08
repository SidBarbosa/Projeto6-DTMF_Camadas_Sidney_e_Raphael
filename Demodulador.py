import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import time 
import sounddevice as sd
from suaBibSignal import *
from scipy.io import wavfile

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 44100

sp,audio = wavfile.read("SIU_modulado.wav")
signal = signalMeu()
signal.plotFFT(audio, fs)

order = 11
tempo = np.arange(0, len(audio)/fs,1/fs)
carier = np.cos(2*np.pi*14000*tempo)

plt.show()

audio_demodulado = audio*carier
x2,f2 = signal.calcFFT(audio_demodulado, fs)

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.plot(tempo, audio_demodulado)
plt.title("Sinal Demodulado - Domínio do Tempo")
plt.xlabel("Tempo [s]")
plt.ylabel("Sinal")
plt.grid()
plt.subplot(2, 1, 2)
plt.plot(x2, f2)
plt.title("Transformada de Fourier do Sinal Demodulado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.show()

audio_filtro3k = butter_lowpass_filter(audio_demodulado, 3000, fs, order)

Siu_final = wavfile.write("SIU_final.wav", fs, audio_filtro3k.astype(np.int16))

x3,f3 = signal.calcFFT(audio_filtro3k, fs)
plt.plot(x3, f3)
plt.title("Transformada de Fourier do Sinal Demodulado Filtrado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.show()



