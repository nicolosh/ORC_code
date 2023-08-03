#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" --------- MULTILINE COMMENT .............
Created on Tue Oct  4 11:15:12 2022

@author: student
"""

''' ----------- IMPORTING STUFF -------------- '''

from math import sqrt
'''from math import *''' # importing everything
# import math as mate # in order to use a library with the name we want
# import math
'''----------------------- '''

print("Python_Tutorial\n")

# CREATES the x variable (SINGLE LINE comment)
''' or we can use single quotes'''

x = 3.543113
print("x = ", x, "the end. \n")

condition = x > 0
condition = True #or False (capital letters!)

if(condition):
    print("x is positive\n")
    x = x + 1
    print(condition, "\n")
else:
    print("x is negative\n")
    print(condition, "\n")
    
    
'''............LIST OF NUMBERS and FOR Loops..............'''
    
#for i in range(5):
#    print(i)
    
# to commet few lines: select them, then ctrl + 1
    
for i in range(3,8):
    print(i, "\n")
    
''' ------------ LIST (LIKE MORE OR LESS ARRAYS) --------------'''

x = [3, 8, 9, 1, 3] # WE CAN DO slicing x[i:j] or x[i:] or x[:j]

x.append(10) # 1st mode to append

x = x + [3] #2nd mode to append

z = x[:3] + x[-3:] #concatenating lists
print("z = ", z, "\n")

z[3] = 17 #modifying the list

''' T-uple ''' # NOT MODIFYABLE OBJECTS --> WON'T USE THEM much
c = (1,312, 12,112) 

''' -------------WHILE LOOP --------------------'''

i = 1
while(i<10):
    print("i =", i, "\n")
    i += 1
    
    
    
k = None # like NULL pointer in C/C++

print(k, "\n")

''' --------- FUNCTIONS ------- '''

def absolute(x):
    if(x < 0):
        return -x
    return x
    

v = absolute(-12)
print("absolute(-12) =", v, "\n")
    

def maxi(x, y = 0, z = 0):
    if(x > y and x > z):
        return x
    if(y > x and y > z):
        return y
    return (x, z) # TO RETURN MULTIPLE VALUES as t-uples

print("maxi(x = 1, z = 5) =", maxi(x = 1, z = 5), "\n")


''' ------------- CLASSES ------------- '''  

#Starting from structs to classes

#struct Point2D
#    int x = 0, y = 0
#    
#    def norm():
#        return 0
#    


class Point2D:
    def __init__(self, x = 0, y = 0):  # Constructor: called when creating an isntance/object of the data class/struct
        self.x = x
        self.y = y
        
    # self is a pointer to the object itself (equivalent to "this" in C++)
    
    def norm(self): #function (method) belonging to the class/struct: inside struct function + struct: CLASS
        return sqrt(pow(self.x, 2) + pow(self.y, 2)) #POWER IN python: ** or pow()
        # return sqrt(self.x**2 + self.y**2) # 2nd method to return norm()



point = Point2D(3, 4)
print("Point (3, 4) norm is: ", point.norm(), "\n")