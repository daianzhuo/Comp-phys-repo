# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 12:30:18 2018

@author: Anzhuo Dai
"""

import random
import pylab as pl
import time

random.seed = 20310312
N = 1e5
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
    return l, N/bins

def sine_pdf(x):    
    """
    used to plot the pdf later
    """
    return 0.5*pl.sin(x)

def transformation(N, mini, maxi, bins):
    start_time = time.time()
    
    a = uniform(N, mini, maxi, bins)[0]
    f = lambda x: pl.arccos(1 - 2 * x) #implements calculated cdf
    l = [f(i) for i in a]
    
    print("Time for transformation method with %s points: %s" %(N, time.time() - start_time))
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
    acc_no = 0         #number of points accepted
    for x in generator:
        y = random.uniform(0, 1)
        if y < pdf(x): #condition for acceptance
            accepted.append(x)
            acc_no += 1
        if acc_no == N:
            break
        
    #print("Time for " + mode + " rejection method with %s points: %s" %(N, (time.time() - start_time)))
    return accepted, time.time()-start_time
  
def time_test(trials):
    """
    finds time ratio for 1000 points and 1000 cycles to get an average
    """
    ratio = []
    for i in range(int(trials)):
        st = rejection("sine", 1000, 0, pl.pi)[1]
        ut = rejection("uniform", 1000, 0, pl.pi)[1]
        ratio.append(st/ut)
    return pl.average(ratio)

print(time_test(1000)) #<------comment out to run faster

a = uniform(N, mini, maxi, bins)

pl.figure()
pl.hist(a[0], bins = 100, edgecolor='black', linewidth = 1.0)
#pl.hlines(a[1], mini, maxi, color = "black", linewidth = 3.0, label = "uniform distribution")
pl.legend()

pl.figure()
pl.hist(transformation(N, mini, maxi, bins), bins, edgecolor='black', linewidth=1.0)
#x = pl.linspace(0,pl.pi,1000)
#pl.plot(x, sine_pdf(x)*10500, color = "black", linewidth = 3.0, label = r'$\frac{1}{2} \sin(x)$')
pl.legend()

b = rejection("sine", 100000, 0, pl.pi)[0]
pl.figure()
#pl.hist(b, bins = 30, edgecolor='black', linewidth=1.0)


"""
plotting for rejection method, code has same functionality as the above function, just more messy and use to plot stuff
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
    a = accepted
    return a, xx, yy

pl.figure()
a, xx, yy = rejection_edited("uniform", 6000, mini, pl.pi)
pl.plot(xx, yy, "x", label = "sine comparison function")
pl.plot(pl.linspace(0, pl.pi, 100), sine_sqr_pdf(pl.linspace(0, pl.pi, 100)), 'black', linewidth = 2, label = r"$\frac{2}{\pi} \sin^2(x)$")
pl.legend(loc = 1)

pl.figure()
a, xx, yy = rejection_edited("sine", 6000, mini, pl.pi)
pl.plot(xx, yy, "x", label = "sine comparison function")
pl.plot(pl.linspace(0, pl.pi, 100), sine_sqr_pdf(pl.linspace(0, pl.pi, 100)), 'black', linewidth = 2, label = r"$\frac{2}{\pi} \sin^2(x)$")
pl.legend(loc = 1)
