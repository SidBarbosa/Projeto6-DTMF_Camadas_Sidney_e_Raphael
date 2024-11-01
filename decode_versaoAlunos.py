
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 

    #Gd = 0.000214z+0.0002111/z^2 - 1.959 + 0.9592 -> Funcao de transferencia discretizada considerando 1000 como wc
    a = 0.000214
    b = 0.0002111
    d = -1.959
    e = 0.9592
    



       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 48000#taxa de amostragem
    sd.default.channels = 1 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.
    duration =  3 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic   
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
    numAmostras = int(duration*sd.default.samplerate)
    freqDeAmostragem = sd.default.samplerate
    #A seguir, faca um print informando que a gravacao foi inicializada
    print("Gravacao comecando e 2 segundos")
    time.sleep(2)
    print("Gravando...")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("Gravacao finalizada")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, ou uma lista, ou ainda uma lista de listas (isso dependerá do seu sistema, drivers etc...).
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    audio = audio[:, 0]
    #t = np.linspace(0, duration, numAmostras)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .

    # Plotando o sinal de áudio capturado
    # plt.figure()
    # plt.plot(t[1000:], audio[1000:])  
    # plt.title("Áudio capturado - Domínio do Tempo")
    # plt.xlabel("Tempo [s]")
    # plt.ylabel("Amplitude")
    # plt.show() 

    
    ## Calcule e plote o Fourier do sinal audio. como saída tem-se a amplitude e as frequências.
    fs = 48000
    xf, yf = signal.calcFFT(audio, fs)   

    # Plotando o sinal no domínio da frequência (Fourier)
    # plt.figure()
    # plt.plot(xf, yf)
    # plt.title("Transformada de Fourier do Sinal Gravado")
    # plt.xlabel("Frequência [Hz]")
    # plt.ylabel("Magnitude")
    # plt.show() 

    #Agora você terá que analisar os valores xf e yf e encontrar em quais frequências estão os maiores valores (picos de yf) de da transformada.
    #Encontrando essas frequências de maior presença (encontre pelo menos as 5 mais presentes, ou seja, as 5 frequências que apresentam os maiores picos de yf). 
    #Cuidado, algumas frequências podem gerar mais de um pico devido a interferências na tranmissão. Quando isso ocorre, esses picos estão próximos. Voce pode desprezar um dos picos se houver outro muito próximo (5 Hz). 
    #Alguns dos picos  (na verdade 2 deles) devem ser bem próximos às frequências do DTMF enviadas!
    #Para descobrir a tecla pressionada, você deve encontrar na tabela DTMF frquências que coincidem com as 2 das 5 que você selecionou.
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    entrada = audio
    saida = [0]*len(entrada)
    saida[1] = a*entrada[0]

    for k in range(2,len(entrada)):
        saida[k] = -d*saida[k-1] - e*saida[k-2] + a*entrada[k-1] + b*entrada[k-2]


    # Plot do Fourier do sinal filtrado
    xfs, yfs = signal.calcFFT(saida, fs)

    plt.figure(figsize=(10, 10))
    plt.subplot(2, 1, 1)
    plt.plot(xf, yf)
    plt.title("Transformada de Fourier do Sinal Gravado")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Magnitude")
    plt.subplot(2, 1, 2)
    plt.plot(xfs, yfs)
    plt.title("Transformada de Fourier do Sinal Filtrado")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Magnitude")
    plt.show()



    # # Identificar os picos na Transformada de Fourier
    indexes = peakutils.indexes(yf, thres=0.4, min_dist=45)
    freqs_de_pico = xf[indexes]
    
    indexes = peakutils.indexes(yfs, thres=0.4, min_dist=45)
    freqs_de_pico_filtrado = xfs[indexes]
    
    # #printe os picos encontrados! 
    # print('Teste', len(indexes))
    # if len(indexes) < 5:
    #     print(f"Menos de 5 picos identificados ({len(indexes)} picos), ajustando parâmetros.")
    #     # Ajusta os parâmetros novamente para detectar mais picos, se necessário
    #     indexes = peakutils.indexes(yf, thres=0.05, min_dist=30)
    #     freqs_de_pico = xf[indexes]

    # print("Frequências identificadas nos picos: ", freqs_de_pico)
    # print("Frequências identificadas nos picos filtrados: ", freqs_de_pico_filtrado)

    
    # #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla

    # Identificar quais frequências DTMF correspondem aos picos
    dtmf_frequencies = {
        '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
        '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
        '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
     }

    # Encontrar a tecla pressionada
    for tecla, (f1, f2) in dtmf_frequencies.items():
            if any(abs(f - f1) < 5 for f in freqs_de_pico) and any(abs(f - f2) < 5 for f in freqs_de_pico):
                print(f"Tecla pressionada: {tecla}")
                break
        #print o valor tecla!!!
        #Se acertou, parabens! Voce construiu um sistema DTMF
    # # Encontrar a tecla pressionada
    # for tecla, (f1, f2) in dtmf_frequencies.items():
    #     if any(np.isclose(freqs_de_pico, f1, atol=5)) and any(np.isclose(freqs_de_pico, f2, atol=5)):
    #         print(f"A tecla pressionada foi: {tecla}")
    #         break

    # #print o valor tecla!!!
    # #Se acertou, parabens! Voce construiu um sistema DTMF

        # #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

        
        # ## Exiba gráficos do fourier do som gravados 
    # plt.show()

if __name__ == "__main__":
    main()
from scipy.signal import windows as window


