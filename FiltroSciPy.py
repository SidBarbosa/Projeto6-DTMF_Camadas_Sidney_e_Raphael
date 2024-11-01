import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import time 
import sounddevice as sd
from suaBibSignal import *


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y



order = 11 #Quanto maior a ordem mais "rapido" acontece a queda da frequencia (relacionada com o comportamento das funcoes de acordo com o crescimento da ordem)
fs = 48000     #Frequencia do proprio microfone
cutoff = 1000  #Frequencia que definimos para corte


b, a = butter_lowpass(cutoff, fs, order=2)
b2, a2 = butter_lowpass(cutoff, fs, order)

w, h = freqz(b, a, fs=fs, worN=8000)
w2, h2 = freqz(b2, a2, fs=fs, worN=8000)

plt.figure(figsize=(10, 7))
plt.subplot(2, 1, 1)
plt.plot(w, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.05*fs)
plt.title("Filtro Passa Baixa")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(w2, np.abs(h2), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.05*fs)

plt.xlabel('Frequencia [Hz]')
plt.grid()
plt.show()



signal = signalMeu() 
print("Gravacao comecando e 2 segundos")
time.sleep(2)
print("Gravando...")
audio = sd.rec(int(3*fs), fs, channels=1)
sd.wait()
print("Gravacao finalizada")

audio = audio[:, 0]
xf, yf = signal.calcFFT(audio, fs) #Fourier sem filtro
saida = butter_lowpass_filter(audio, cutoff, fs, order)
xf2, yf2 = signal.calcFFT(saida, fs) #Fourier com filtro


plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.plot(xf, yf)
plt.xlim(0, 0.1*fs)
plt.title("Transformada de Fourier do Sinal Gravado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.grid()
plt.subplot(2, 1, 2)
plt.plot(xf2, yf2)
plt.xlim(0, 0.1*fs)
plt.title("Transformada de Fourier do Sinal Filtrado")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude")
plt.grid()
plt.show()




