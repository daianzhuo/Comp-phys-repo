# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:37:54 2018

@author: Andrew.Dai
"""

import pylab as pl
from scipy import integrate
import time

pdw = lambda z: (1/pl.pi**0.5)*(pl.e**(-z**2))

convergence = lambda I1, I2: pl.absolute((I2-I1)/I1)

x = pl.linspace(0,2,262145)
y = pdw(x)
pyint = integrate.trapz(y,x)


def trapezoidal_rule_generator(f, start, stop, ε):
    I1 = (stop - start) * 0.5 * (f(start) + f(stop))
    I2 = I1/2 + f((stop-start)/2)*(stop-start)/2
    h = stop - start
    while True:
        I1 = I2
        h *= 0.5
        N = int((stop - start)/h) + 1
        z = pl.linspace(start, stop, N) #create evenly spaced z values to be put into function
        sigma = sum([f(z[2*i + 1]) for i in range(0, int((N-1)/2))])
        I2 = 0.5 * I1 + h * sigma
        yield I1, I2, N

def trapezoidal_rule(f, start, stop, ε):
    for I1, I2, N in trapezoidal_rule_generator(f, start, stop, ε):
        if convergence(I1, I2) < ε:
#            print(N)
            return I2
        
t = trapezoidal_rule(pdw,0,2,1e-6)

def simps(f, start, stop, ε):
    for I1, I2, N in trapezoidal_rule_generator(f, start, stop, ε):
        area = (4/3) * I2 - (1/3) * I1
        if convergence(I1, I2) < ε:
#            print(N) 
            return area

s = simps(pdw,0,2,1e-6)

print(pyint - t)
print(pyint - s)


#def trapezoidal_rule(f, start, stop, ε):
#    i = 0 #number of iterations
#    I1 = (stop - start) * 0.5 * (f(start) + f(stop))
#    I2 = I1/2 + f((stop-start)/2)*(stop-start)/2
#    h = stop - start
#    while True:
#        I1 = I2
#        i += 1
#        h *= 0.5
#        N = int((stop - start)/h) + 1
#        z = pl.linspace(start, stop, N) #create evenly spaced z values to be put into function
#        sigma = sum([f(z[2*i + 1]) for i in range(0, int((N-1)/2))])
#        I2 = 0.5 * I1 + h * sigma
#        if convergence(I1, I2) < ε:
#            print(N)
#            return I2