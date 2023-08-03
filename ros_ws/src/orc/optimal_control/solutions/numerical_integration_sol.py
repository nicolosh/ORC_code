#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 11:53:57 2021

@author: adelprete
"""
import numpy as np
from numpy.linalg import norm, solve


def rk1(x, h, u, t, ode, jacobian=False):
    if(jacobian==False):
        dx = ode.f(x, u, t)
        x_next = x + h*dx
        return x_next, dx

    (f, f_x, f_u) = ode.f(x, u, t, jacobian=True)
    dx = f
    x_next = x + h*f
    
    nx = x.shape[0]
    I = np.identity(nx)    
    phi_x = I + h*f_x
    phi_u = h * f_u
    return x_next, dx, phi_x, phi_u

# u is constant through the time step!
def rk2(x, h, u, t, ode):
    k1 = ode.f(x, u, t)
    k2 = ode.f(x + 0.5*h*k1, u, t + 0.5*h)
    
    dx = k2
    x_next = x + h * k2
    return x_next, dx

def rk2heun(x, h, u, t, ode):
    k1 = ode.f(x, u, t)
    k2 = ode.f(x + h*k1, u, t + h)
    
    dx = 0.5*(k1 + k2)
    x_next = x + 0.5*h*(k1 + k2)
    return x_next, dx

# Kutta's third order method
def rk3(x, h, u, t, ode):
    k1 = ode.f(x, u, t)
    k2 = ode.f(x + 0.5*h*k1, u, t + 0.5*h)
    k3 = ode.f(x + h * (-k1 + 2*k2), u, t + h)
    
    dx = 1/6*k1 + 2/3*k2 + 1/6*k3
    x_next = x + h * (1/6*k1 + 2/3*k2 + 1/6*k3)
    return x_next, dx


#TO CHECK !!!!!    ---------------------------------------------------------
def rk4(x, h, u, t, ode, jacobian=False):
    xi2 = x + 0.5*h*k1
    xi3 = x + 0.5*h*k2
    xi4 = x + h*k3
    
    k1 = ode.f(x, u, t)
    k2 = ode.f(xi2, u, t + 0.5*h)
    k3 = ode.f(xi3, u, t + 0.5*h)
    k4 = ode.f(xi4, u, t + h)
    
    dx = 1/6*k1 + 1/3*k2 + 1/3*k3 + 1/6*k4
    x_next = x + h * (1/6*k1 + 1/3*k2 + 1/3*k3 + 1/6*k4)
        
    if(not jacobian):        
        #DERIVATIVES OF C.T dynamics
        (f, f_xi, f_ui)   = ode.f(x,   u, t, jacobian=True)
        (f, f_xi2, f_ui2) = ode.f(xi2, u, t, jacobian=True)
        (f, f_xi3, f_ui3) = ode.f(xi3, u, t, jacobian=True)
        (f, f_xi4, f_ui4) = ode.f(xi4, u, t, jacobian=True)
        
        nx = x.shape[0]
        I = np.identity(nx)    
        
        dk1dxi = f_xi
        dk2dxi = f_xi2*(I + 0.5*h*dk1dxi)
        dk3dxi = f_xi3*(I + 0.5*h*dk2dxi)
        dk4dxi = f_xi4*(I + h*dk3dxi)        
    
        dk1dyi = f_ui
        dk2dyi = f_xi2*(0.5*h*dk1dyi) + f_ui2
        dk3dyi = f_xi3*(0.5*h*dk2dui) + f_ui3
        dk4dyi = f_xi4*(h*dk3dui)     + f_ui4
        
        phi_x = I + 1/6 * h * (dk1dxi + 2dk2dxi + 2dk3dxi + dk4dxi)
        phi_u = 1/6 * h * (dk1dyi + 2*dk2dyi + 2*dk3dyi + dk4dyi)
        
        return x_next, dx, phi_x, phi_u
    
    return x_next, dx

# Not purpose of the course
def semi_implicit_euler(x, h, u, t, ode):
    return x_next, dx

def implicit_euler(x, h, u, t, ode):
    return x_next, dx