# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 11:45:37 2018

@author: Anzhuo Dai
"""

import pylab as pl
import numpy.fft

x1 = -8
x2 = 8
N = 2**17 #to increase FFT efficiency
t = pl.linspace(x1, x2, N)
T = x2-x1
dT = T/N
print("Nyquist frequency is " + str(pl.pi/dT))

def tophat(t, left, right):
    h = []
    for i in t:
        if i < float(left):
            h.append(0)
        elif i >= float(left) and i <= float(right):
            h.append(4)
        elif i > float(right):
            h.append(0)
    return h

def gaussian(t):
    return (1/pl.sqrt(2*pl.pi)) * pl.exp(-t**2/2)

def split_gaussian(t):
    """
    splits gaussian into two parts at the ends of the range used so when
    convolved it returns correctly centered function
    """
    tt = t.tolist()
    split = int(len(tt)/2) #splits list halfway
    t_new = tt[split:] #adds second half as the first half of new list
    tremain = t[split:].tolist()
    tremain.reverse() #reverses second half
    for i in tremain:
        t_new.append(i) #put reversed second half into new list
    gt = [gaussian(i) for i in t_new] #calculate the split gaussian
    return gt
    
def convolve(f, g):
    ftilda = numpy.fft.fft(f) #FT of f
    gtilda = numpy.fft.fft(g) #FT of g
    convolution = numpy.fft.ifft(pl.multiply(ftilda, gtilda)) #Convolution using properties of fourier transforms and convolution
    return pl.divide(convolution, len(ftilda)) * T
  
a = tophat(t, 3, 5)
b = gaussian(t).tolist()
c = split_gaussian(t)

pl.figure("h(t)")
pl.plot(t, a, label = "h(t)")
pl.plot(t, b, label = "g(t)")
#pl.figure("convolution")
pl.plot(t, convolve(a, c), label = "h(t)*g(t)")
pl.legend()


print(pl.trapz(convolve(a,c), t, dx = 0.0001)) #finds area under convolution curve

pl.figure()
pl.plot(pl.fftfreq(N, d = dT), numpy.fft.fft(a), label = r"$\mathcal{F}(h(t))(\omega)$")
pl.legend()
pl.figure()
pl.plot(pl.fftfreq(N, d = dT), numpy.fft.fft(b), label = r"$\mathcal{F}(g(t))(\omega)$")
pl.legend()
