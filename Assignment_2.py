# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 21:27:01 2018

@author: Andrew.Dai
"""

import sys
sys.path.insert(0, "C:\\Users\\Andrew.Dai\\Documents\\My files\\Yr3 Computational physics\\Problem sheets\\")
from PS3_matrix import Matrix

import pylab as pl
import numpy as np

asgmt = np.matrix([[3,1,0,0,0], [3,9,4,0,0], [0,9,20,10,0], [0,0,-22,31,-25], [0,0,0,-55,60]])
b = np.matrix([[2], [5], [-4], [8], [9]])

def crouts(A):
    ni = len(A)
    L = pl.zeros((ni, ni))
    U = pl.zeros((ni, ni))
    pl.fill_diagonal(L, 1)
    
    for j in range(ni):
        for i in range(j+1):
            sigma1 = 0
            for k in range(i):
                sigma1 += L[i][k] * U[k][j]
            U[i][j] = A[i,j] - sigma1
        
        for i in range(j+1, ni):
            sigma2 = 0
            for k in range(j):
                sigma2 += L[i][k] * U[k][j]
            L[i][j] = (1 / U[j][j]) * (A[i,j] - sigma2)
           
    return L, U

def determinant(U):
    return pl.product([U[i][i] for i in range(len(U))])

def solvex(A,b):
    L, U = crouts(A)
    ni = len(L)
    y = pl.zeros((ni, 1))
    y[0][0] = b[0][0] #/L[0][0] but L[0][0] = 1
    for i in range(1,ni):
        sigma1 = 0
        for j in range(i):
            sigma1 += L[i][j] * y[j][0]
        y[i][0] = (b[i][0] - sigma1) / L[i][i]
        
    x = pl.zeros((ni, 1))
    x[-1][0] = y[-1][0] / U[-1][-1]
    order = [i for i in range(ni-1)]
    order.reverse()
    for i in order:
        sigma2 = 0
        for j in range(i+1, ni):
            sigma2 += U[i][j] * x[j][0]
        x[i][0] = (y[i][0] - sigma2) / U[i][i]
    return x

def inverse(A):
    ni = len(A)
    I = pl.zeros((ni, ni))
    pl.fill_diagonal(I, 1)
    #extract columns as solvex can only process 1 column at a time for x and b
    inv_dummy = []
    for c in range(ni):
        i = I[:,c]
        b = np.matrix([[entry] for entry in i])
        inv_dummy.append(solvex(A,b))

    a = []
    for i in inv_dummy:
        a.append(i.reshape((1,len(i)))[0].tolist())
    
    b = []
    for j in zip(*a):
        b.append(j)
        
    inv = np.matrix(b)
    return inv


L, U = crouts(asgmt)
print(determinant(U))
#x = solvex(asgmt,b)

#print(x)
#print(pl.matmul(asgmt, x))
#print(pl.matmul(inverse(asgmt), asgmt))
print(inverse(asgmt))