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

signal = signalMeu() 

order = 11 #Quanto maior a ordem mais "rapido" acontece a queda da frequencia (relacionada com o comportamento das funcoes de acordo com o crescimento da ordem)
fs = 44100     
cutoff = 3000  


sp, data = wavfile.read("SIU.wav")
audio = data[:,0]
audio_filtro3k = butter_lowpass_filter(audio, cutoff, fs, order)

tempo = np.arange(0, len(audio_filtro3k)/fs,1/fs)


x1,y1 = signal.calcFFT(audio_filtro3k, fs)


plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.plot(tempo, audio_filtro3k)
plt.title("Sinal Filtrado - Domínio do Tempo")
plt.xlabel("Tempo [s]")
plt.ylabel("Sinal")
plt.grid()
plt.subplot(2, 1, 2)
plt.title("Transformada de Fourier do Sinal Filtrado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.plot(x1, y1)
plt.show()



filtrado_wav = wavfile.write("SIU_filtrado.wav", fs, audio_filtro3k.astype(np.int16))


carier = np.cos(2*np.pi*14000*tempo)

modulado = audio_filtro3k*carier
x2,y2 = signal.calcFFT(modulado, fs)

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.plot(tempo, modulado)
plt.title("Sinal Modulado - Domínio do Tempo")
plt.xlabel("Tempo [s]")
plt.ylabel("Sinal")
plt.grid()
plt.subplot(2, 1, 2)
plt.title("Transformada de Fourier do Sinal Modulado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.plot(x2, y2)
plt.show()

constante = max(abs(modulado))

modulado_wav = wavfile.write("SIU_modulado.wav", fs, modulado.astype(np.int16))

normalizado = modulado/constante

normalizado_wav = wavfile.write("SIU_normalizado.wav", fs, normalizado.astype(np.int16))

plt.plot(tempo, normalizado)
plt.title("Sinal Modulado Normalizado - Domínio do Tempo")
plt.xlabel("Tempo [s]")
plt.ylabel("Sinal")
plt.show()
