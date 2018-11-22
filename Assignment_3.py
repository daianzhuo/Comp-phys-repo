# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:07:05 2018

@author: Anzhuo Dai
"""

from Assignment_2 import solvex
import pylab as pl
import time
import scipy as sp

start_time = time.time()

x = [-2.1, -1.45, -1.3, -0.2, 0.10, 0.15, 0.8, 1.1, 1.5, 2.8, 3.8]
f = [0.012155, 0.122151, 0.184520, 0.960789, 0.990050, 0.977751, 0.527292, 0.298197, 0.105399, 3.936690e-4, 5.355348e-7]

def linear_interp(x,f,n): #n is number of points wanted between points
    if len(x) != len(f):
        raise Exception("inputs do not have the same length")
    
    #lists for new coordiantes
    x_new = []
    f_new = []
    for i in range(len(x)-1):
        xstep = (x[i+1] - x[i]) / n #the step size in x for new points
        line = lambda X: ((x[i+1] - X) * f[i] + (X - x[i]) * f[i+1]) / (x[i+1] - x[i]) #defines the straight line between two points
        dummyx = []
        for j in range(n):
            x_new.append(x[i] + xstep * j) #calculates new x values, could have used pl.linspace but I'm scared it could screw things up somehow
            dummyx.append(x[i] + xstep * j) #appends to separate list to accomodate the different line equations
        for a in dummyx:
            f_new.append(line(a)) #calculates new y values
        
    x_new.append(x[-1])
    f_new.append(f[-1])
    return x_new, f_new

def cubic_spline(x, f, n):
    #first construts matrices M and F to solve for d in M*d=F
    
    N = len(f) #length of data, not to be confused with n
    
    #setup F vector 
    Fi = lambda i: (f[i+1] - f[i])/(x[i+1] - x[i]) - (f[i] - f[i-1])/(x[i] - x[i-1]) #only using lambda for cleaniness' sake
    F = [Fi(i) for i in range(1, N-1)]
    F = [[i] for i in F]

    #prepare a, b, c to fill into M
    a = [(x[i] - x[i-1]) / 6 for i in range(2, N-1)]
    b = [(x[i+1] - x[i-1]) / 3 for i in range(1, N-1)]
    c = [(x[i+1] - x[i]) / 6 for i in range(1, N-2)]
    
    #now set up big boi tridiagonal matrix M
    M = pl.zeros((N-2, N-2))
    for i in range(len(a)):
        M[i+1][i] = a[i]
        M[i][i+1] = c[i]
    pl.fill_diagonal(M, b)
    
    #finally, solve for d
    Fpp = solvex(M, F)
    Fpp = Fpp.tolist()
    
    #boundary conditions for natural spline
    Fpp.insert(0, [0.]) #add 0. to the beginning
    Fpp.append([0]) #and to the end
    Fpp = pl.array(Fpp) #return to array form

    #i needs to be the index of the first point to the left of new x value so x_new is between x[i] and x[i+1]
    A = lambda X, i: (x[i+1] - X) / (x[i+1] - x[i])
    B = lambda X, i: 1 - A(X, i)
    C = lambda X, i: (A(X, i) ** 3 - A(X, i)) * ((x[i+1] - x[i]) ** 2) / 6
    D = lambda X, i: (B(X, i) ** 3 - B(X, i)) * ((x[i+1] - x[i]) ** 2) / 6
    
    line = lambda X, i: A(X, i) * f[i] + B(X, i) * f[i+1] + C(X, i) * Fpp[i] +D(X, i) * Fpp[i+1] #spline equation
    
    x_new = []
    f_new = []    
    for j in range(N-1):
        x_new_chunk = pl.linspace(x[j], x[j+1], n) #creates x values
        f_new_chunk = [line(X, j) for X in x_new_chunk] #and y values
        x_new.append(x_new_chunk)
        f_new.append(f_new_chunk)

    #unpack sublists in lists
    x_new = [item for sublist in x_new for item in sublist]
    f_new = [item for sublist in f_new for item in sublist]
    
    return x_new, f_new

cs = cubic_spline(x, f, 100)

pl.figure("Assignment_3")
pl.plot(x,f,"o", label = "original points")
pl.plot(linear_interp(x,f,10)[0], linear_interp(x,f,10)[1], linewidth = 2, label = "linear interpolation")

test = sp.interpolate.interp1d(x,f, kind = 'cubic')
pl.plot(cs[0], test(cs[0]), label = "scipy.interpolate cubic") #test against scipy's cubic spline
    
pl.plot(cs[0], cs[1], label = "cubic spline")
pl.xlabel("x")
pl.ylabel("f")
pl.legend()


print('Time taken to run: %s' %(time.time() - start_time))