#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:24:03 2022

@author: student
"""

import numpy as np

''' ------- NUMPY introduction (doing LINEAR ALGEBRA stuff) ---------- '''

print("Numpy_tutorial\n")

x = np.zeros(3)
y = np.array([3., 6., 12.])

x = x + 1

print("x =", x, "\n")

def increment(a):
    a = np.copy(a) # USEFUL HINT: do this to not modify what should not be modified
    a = a + 1
    return a

# creating matrices

A = np.zeros((3,3))

AS = A.shape
xS = x.shape

print("x shape: ", xS, " - A shape: ", AS, "\n")

I = np.identity(3)

# dot product: 3 different ways of doing it
first = I.dot(y)

second = np.dot(I, y)

third = I @ y


B = np.empty((3, 4))*np.nan # trick to check for errors when creating new vectors or matrices

# when passing something to a function or to  a method we are not creating a copy of that object
# but we are passing the reference to that object

increment(y)

np.max(y)

np.min(y)

np.mean(y)

np.abs(y)

np.linalg.norm(y) #c ompute the 2-Norm of y

A = np.random.rand(3, 3)

H = np.linalg.inv(A)


# check

H @ A

A @ H  

# pseudo inverse
B = np.random.rand(2, 3)

Bpseudo_inv = np.linalg.pinv(B)

B @ Bpseudo_inv

Bpseudo_inv @ B

np.floor(B)

np.ceil(B)

np.concatenate((x, y))

B.reshape((6, 1))

B.reshape((3, 2))

B = B.reshape((3, 2)) #override the values of original B matrix

np.arange(5)

np.arange(1, 5)

np.arange(1.5, 5.5)


