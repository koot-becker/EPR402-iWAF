#ESP 410 - Prakties 2 - Simulations
#Group 21
#Created: 28 April 2021
#Stefan Buys, Gerhard Davel, Gerdus Kemp

import numpy as np
import matplotlib.pyplot as plt

Fs = 80000

fc = 0.028125
wc = 2 * np.pi * fc

numPoints = 295

helfde = (numPoints - 1) / 2

hd = [0] * numPoints

wn = [0] * numPoints

freqSteps = np.linspace(0, Fs, num=numPoints*10)
dataPoints = np.linspace(0, 10 * numPoints / Fs, 10 * numPoints)

for i in range(numPoints):
    if not(i == helfde):
        hd[i] = 2.0 * fc * np.sin((i - helfde) * wc) / ((i - helfde) * wc)
    else:
        hd[i] = 2 * fc

    """Window Function"""
    wn[i] = 0.42 + 0.5 * np.cos((2 * np.pi * (i - helfde)) / (numPoints - 1)) + 0.08 * np.cos(
        (4 * np.pi) / (numPoints - 1))
    # wn[i] = 0.54 + 0.46*np.cos((2*np.pi*(i-helfde))/numPoints)
        
print("Impulse Response:")
for i in range(numPoints):
    print("hd(" + str(i) + ") = " + str(hd[i]))


print("Window Function:")
for i in range(numPoints):
    print("wn(" + str(i) + ") = " + str(wn[i]))
    

"""Finale Filter Impulse Response:"""
    
h = [0] * numPoints
    
print("Finale Filter Impulse Response:")
for i in range(numPoints):
    h[i] = hd[i] * wn[i]
    #print("h(" + str(i) + ") = " + str(hd[i] * wn[i]))
    
    
"""Finale Filter Frequency Response:"""
#Calculate the inverse FFT of h:
h_for_fft = h + ([0] * 9 * numPoints)
#print(h_for_fft)
H_fft = np.fft.fft(h_for_fft)
H_fft = abs(H_fft)
H_pow = [0] * (numPoints * 10)

for i in range(numPoints * 10):
    magnitude = np.sqrt(np.power(np.real(H_fft[i]), 2) + np.power(np.imag(H_fft[i]), 2))
    H_pow[i] = 20.0 * np.log10(H_fft[i])
    
"""PLOTTING"""
#Plotting the impulse response
plt.figure(1)
#plt.title("Impulse Response of the Digital Filter")
plt.xlabel("Sample Number")
plt.ylabel("w(n)")
plt.plot(range(numPoints), h)
plt.xlim(0, numPoints)

"""Plotting the Frequency Response:"""
plt.figure(2)
#plt.title("Frequency Response of the Digital Filter")
plt.xlabel("Frequency (Hz)")
plt.ylabel("|W(f)| (dB)")
plt.xlim(1000, 4000)
plt.ylim(-125, 2)
plt.plot(freqSteps, H_pow)
plt.show()


def plotResponses(freq, num):
    sine = [0] * numPoints * 10

    filtered = [0] * numPoints * 10

    for i in range(numPoints * 10):
        sine[i] = 0.5 * np.sin(2 * np.pi * freq * i / Fs)

    """Frequency spectrum of sine wave"""
    fftSine = abs(np.fft.fft(sine))
    fftPow = [0] * numPoints * 10
    filteredPow = [0] * numPoints * 10
    for i in range(numPoints * 10):
        fftPow[i] = 20.0 * np.log10(fftSine[i])
        filtered[i] = fftSine[i] * H_fft[i]
        filteredPow[i] = 20.0 * np.log10(filtered[i])

    output = abs(np.fft.ifft(filtered))

    """Plotting the filter responses"""
    plt.figure(num)
    #plt.title("Time plot of sinusoid")
    plt.xlabel("Time(s)")
    plt.ylabel("Magnitude (V)")
    plt.plot(dataPoints, sine)
    plt.xlim(0, dataPoints[numPoints])

    plt.figure(num + 20)
    #plt.title("Frequency plot of sinusoid")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xlim(0, 20000)
    plt.plot(freqSteps, fftPow)

    plt.figure(num + 40)
    #plt.title("Time plot of filtered sinusoid")
    plt.xlabel("Time(s)")
    plt.ylabel("Magnitude (V)")
    plt.plot(dataPoints, output)
    plt.xlim(0, dataPoints[numPoints])

    plt.figure(num + 60)
    #plt.title("Frequency plot of filtered sinusoid")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xlim(0,20000)
    plt.plot(freqSteps, filteredPow)
    plt.show()


plotResponses(1000, 3)
# plotResponses(1500, 4)
# plotResponses(3000, 5)
# plotResponses(5000, 6)

    
    
    
    
