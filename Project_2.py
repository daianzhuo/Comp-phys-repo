# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:37:54 2018

@author: Andrew.Dai
"""

import pylab as pl
from scipy import integrate
import time

pdw = lambda z: (1/pl.pi**2)*(pl.e**(-z**2))

def trapezoidal_rule(f, start, stop, ε):
    convergence = lambda I1, I2: pl.absolute((I2-I1)/I1)
    i = 0 #number of iterations
    I1 = (stop - start) * 0.5 * (f(start) + f(stop))
    I2 = I1/2 + f((stop-start)/2)*(stop-start)/2
    h = stop - start
    while True:
        I1 = I2
        i += 1
        h *= 0.5
        N = int((stop - start)/h) + 1
#        print(N)
        z = pl.linspace(start, stop, N) #create evenly spaced z values to be put into function
#        print(z)
#        print((N-1)/2)
        sigma = sum([f(z[2*i + 1]) for i in range(0, int((N-1)/2))])
        I2 = 0.5 * I1 + h * sigma
#        print(convergence(I1, I2))
        if convergence(I1, I2) < ε:
            print(N)
            return I2
        
print(trapezoidal_rule(pdw,0,2,1e-6))
x = pl.linspace(0,2,60000)
y = pdw(x)
print(integrate.trapz(y,x))

