# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:44:21 2020

@author: Noé Corneille
"""

import numpy as np

class Vector:
    def __init__(self, elements):
        self.elements = elements
        self.dim = len(elements)
    
    # Checks '<=' element-wise
    def __le__(self, v):
        out = []
        for i in range(0, self.dim):
            out.append(self.elements[i] <= v.elements[i])
        
        return out
    
    def __add__(self, f):
        out = []
        if (type(f) == float) | (type(f) == int):
            for i in range(0, self.dim):
                out.append(self.elements[i] + f)
        elif type(f) == Vector:
            for i in range(0, self.dim):
                out.append(self.elements[i] + f[i])
                
        return Vector(out)
    
    #Returns indices of self.elements == value
    def get_indices(self, value):
        out = []
        for i in range(0, self.dim):
            if self.elements[i] == value:
                out.append(i)
        
        return out

def simulation(dt, num_steps, m, n, N, T1, T2):
    '''
    Parameters
    ----------
    m : int
        number of washing chairs.
    n : int
        number of styling chairs.
    l : float
        parameter of arrivals (poisson distr).
    mu1 : float
        mean washing time (normal).
    sigma1 : float
        sd washing time (normal).
    mu2 : float
        mean styling time (normal).
    sigma2 : float
        sd styling time (normal).

    Returns
    -------
    N_served : int
        number of served people.
    N_blocked : int
        number of blocked people.

    '''
    
    dt = 1/60 # timestep
    num_steps = 1000 # number of steps
    
    tau_1 = Vector([0] * m)
    tau_2 = Vector([0] * n)
    
    wash = Vector(['F'] * m)
    style = Vector(['F'] * n)
    
    N_served = 0 # number of people served
    N_blocked = 0 # number of people blocked
    
    for step in range(0, num_steps):
        # Correct units?
        N_ = N(dt)
        t1 = Vector(T1(dt))
        t2 = Vector(T2(dt))
        
        mask_wash = t1 <= tau_1
        mask_style = t2 <= tau_2
        
        # Serve styling chair people
        for i in range(0, n):
            if mask_style[i]:
                style.elements[i] = 'F'
        
        free_styling_chairs = style.get_indices('F')
        waiting_wash_chairs = wash.get_indices('W')
        
        # Place waiting wash people into styling chairs
        for i in waiting_wash_chairs:
            if len(free_styling_chairs) == 0:
                break
            else:
                wash.elements[waiting_wash_chairs[0]] = 'F'
                style.elements[free_styling_chairs[0]] = 'O'
                
                tau_1.elements[waiting_wash_chairs[0]] = 0
                tau_2.elements[free_styling_chairs[0]] = 0
                
                waiting_wash_chairs.pop(0)
                free_styling_chairs.pop(0)
            
        # Serve washing chair people and place into styling chairs
        for i in range(0, m):
            if mask_wash[i]:
                if len(free_styling_chairs) != 0:
                    wash.elements[i] = 'F'
                    style.elements[free_styling_chairs[0]] = 'O'
                    tau_2.elements[free_styling_chairs[0]] = 0
                    
                    free_styling_chairs.pop(0)
                else:
                    wash.elements[i] = 'W'
        
        # Process arrivals into washing chairs
        free_washing_chairs = wash.get_indices('F')
        served = min(N_, len(free_washing_chairs))
        
        N_blocked += N_ - served
        N_served += served 
        
        for i in range(0, served):
            wash.elements[free_washing_chairs[i]] = 'O'
            tau_1.elements[free_washing_chairs[i]] = 0
            
        tau_1 = tau_1 + dt
        tau_2 = tau_2 + dt
    
    return N_served, N_blocked
    
    