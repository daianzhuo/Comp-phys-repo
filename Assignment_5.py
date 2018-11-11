# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 12:30:18 2018

@author: Andrew.Dai
"""

import numpy as np
import random
import pylab as pl
import time

random.seed = 20310312
N = 1e5
#binsize = 0.1
mini = 0.0
maxi = 1.0
bins = 20

def uniform(N, mini, maxi, bins):
    start_time = time.time()
    counter = 0
    l = []
    while counter != N:
        l.append(random.uniform(mini, maxi)) #generate psudo random number between 0 and 1
        counter += 1
    
    print("Time for uniform dist: %s" %(time.time() - start_time))
    uniform.time = time.time() - start_time
    return l, N/bins

def sine_pdf(x):    
    return 0.5*pl.sin(x)

def transformation(N, mini, maxi, bins):
    start_time = time.time()
    
    a = uniform(N, mini, maxi, bins)[0]
    f = lambda x: pl.arccos(1 - 2 * x)
    l = [f(i) for i in a]
    
    print("Time for transformation method: %s" %(time.time() - start_time))
    transformation.time = time.time() - start_time
    return l

def uniform_single(mini, maxi):
    """
    generator function for uniform psudo random numbers from a single seed
    to be used in rejection method
    """
    while True:
        yield random.uniform(mini, maxi)

def sine_single(mini, maxi):
    """
    generator function for psudo random numbers from a single seed
    under pdf = 0.5*pl.sin(x)
    to be used in rejection method
    """
    f = lambda x: pl.arccos(1 - 2 * x)
    while True:
        yield f(random.uniform(mini, maxi))
    
def sine_sqr_pdf(x):
    return (2/pl.pi) * (pl.sin(x)**2)

def rejection(mode, N, mini, maxi):
    start_time = time.time()
    
    if mode == "uniform":
        generator = uniform_single(mini, maxi)
    elif mode == "sine":
        generator = sine_single(mini, maxi)
    
    pdf = lambda x: (2/pl.pi) * (pl.sin(x)**2)
    accepted = []
    acc_no = 0
    for x in generator:
        y = random.uniform(0, 1)
        if y < pdf(x):
            accepted.append(x)
            acc_no += 1
            #print("{0:.0%}".format(acc_no/N) + " complete")
        if acc_no == N:
            break
        
    print("Time for rejection method with %s points: %s" %(N, (time.time() - start_time)))
    rejection.time = time.time() - start_time
    return accepted
    
#a = uniform(N, mini, maxi, bins)
#
#pl.figure()
#pl.hist(a[0], bins = 20, edgecolor='black', linewidth=1.0)
#pl.hlines(a[1], mini, maxi, color = "black", linewidth = 3.0)
#
#pl.figure()
#pl.hist(transformation(N, mini, maxi, bins), bins, edgecolor='black', linewidth=1.0)
#x = pl.linspace(0,1,1000)
#pl.plot(x, sine_pdf(x*pl.pi))
    

uniform(10000, 0, pl.pi, 20)
transformation(10000, 0, pl.pi, 20)
rejection("uniform", 10000, 0, pl.pi)


def timetest(mini, maxi):
    st = time.time()
        
    print(st - time.time())
def timetest1(mini, maxi):
    st = time.time()
    for i in sine_single(mini, maxi):
        print(st - time.time())
        break        


"""
plotting for rejection method
"""
def rejection_edited(mode, N, mini, maxi):
    """
    mode determines the "top" function which is the distribusion for the initial x value
    mode can be "uniform" or "sine"
    """
    if mode == "uniform":
        generator = uniform_single(mini, maxi)
        top_pdf = lambda x: maxi + (x*0)
    elif mode == "sine":
        generator = sine_single(mini, maxi)
        top_pdf = lambda x: 0.5*pl.sin(x)
        
    #start_time = time.time()
    
    pdf = lambda x: (2/pl.pi) * (pl.sin(x)**2)
    xf = []
    xx = []
    yy = []
    accepted = []
    ay = []
    acc_no = 0
    rej_no = 0
    for x in generator:
        xf.append(top_pdf(x))
        xx.append(x)
        y = random.uniform(0, 1)
        yy.append(y)
        if y < pdf(x):
            accepted.append(x)
            ay.append(y)
            acc_no += 1
            #print("{0:.0%}".format(acc_no/N) + " complete")
        else:
            rej_no += 1
        if acc_no == N:
            break
    #print("Time for rejection method: %s" %(time.time() - start_time))
    pl.plot(xx, yy, 'x') #plots initially generated grid
    #pl.plot(accepted, ay, 'o', markersize = 1, label = "accepted points") #plots accepted grid
    pl.plot(pl.linspace(0, pl.pi, 100), top_pdf(pl.linspace(0, pl.pi, 100)), 'black', linewidth = 2, label = r'$\frac{2}{\pi} \sin(x)^2$')
    pl.legend()
    pl.grid()
    
    pl.figure()
    pl.plot()
    
    rejection.acc_no = acc_no
    rejection.rej_no = rej_no
    
    return accepted

#a = rejection_edited("sine", 10000, 0, pl.pi)
#pl.plot(pl.linspace(0, pl.pi, 100), sine_sqr_pdf(pl.linspace(0, pl.pi, 100)), 'black', linewidth = 2, label = "(2/pl.pi)*pl.sin(x)**2")
#pl.hist(a, bins = 20, edgecolor='black', linewidth=1.0)

#print(rejection("uniform", 10000, 0, pl.pi))