# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 11:45:37 2018

@author: Andrew.Dai
"""

import pylab as pl
import numpy.fft

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

def convolve(f, g):
    ftilda = numpy.fft.fft(f)
    gtilda = numpy.fft.fft(g)
    convolution = numpy.fft.ifft(pl.multiply(ftilda, gtilda))
    return pl.divide(convolution, len(ftilda))

t = pl.linspace(-8, 8,100000)
pl.figure("h(t)")
pl.plot(t, tophat(t, 3, 5), label = "h(t)")
pl.figure("g(t)")
pl.plot(t, gaussian(t), label = "g(t)")
pl.figure("convolution")
pl.plot(t, convolve(tophat(t, 3, 5), gaussian(t)))


#pl.legend()