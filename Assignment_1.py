# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 10:17:42 2018

@author: Anzhuo Dai
"""

import time
import pylab as pl

start_time = time.time()

def machine_accuracy():
    b = float(1.0)
    e = 0
    while b - 2**e != 1.0:
        e -= 1
    return e+1

def precision_accuracy():
    b = pl.float16(1.0)
    e16 = 0
    while pl.float16(1.0) - pl.float16(2**e16) != pl.float16(1.0):
        b = b/pl.float16(2)
        e16 -= 1
    
    b = pl.float32(1.0)
    e32 = 0
    while pl.float32(1.0) - pl.float32(2**e32) != pl.float32(1.0):
        b = b/pl.float32(2)
        e32 -= 1

    b = pl.float64(1.0)
    e64 = 0
    while pl.float64(1.0) - pl.float64(2**e64) != pl.float64(1.0):
        b = b/pl.float64(2)
        e64 -= 1
        
    b = pl.longdouble(1.0)
    e128 = 0
    while pl.longdouble(1.0) - pl.longdouble(2**e128) != pl.longdouble(1.0):
        b = b/pl.longdouble(2)
        e128 -= 1

    return e16+1, e32+1, e64+1, e128+1
       
print(machine_accuracy())
print(precision_accuracy())

print('Time taken to run: %s' %(time.time() - start_time))