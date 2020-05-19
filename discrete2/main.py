# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:38:30 2020

@author: 20161443
"""


from discrete_2 import *

def main(dt, num_steps, m, n, distr_params):
    N = lambda x : np.random.poisson(distr_params[0] * x)
    T1 = lambda x : np.random.normal(distr_params[1] * x, distr_params[2] * x, m)
    T2 = lambda x : np.random.normal(distr_params[3] * x, distr_params[4] * x, n)
    
    return simulation(dt, num_steps, m, n, N, T1, T2)



def verify_model_1(dt, num_steps, m, n, c, w, s):    
    # Verify Model 1
    N = lambda x : np.random.binomial(n = 1, p = c)
    T1 = lambda x : 1E9 * np.random.binomial(size = m, n = 1, p = 1-w)
    T2 = lambda x : 1E9 * np.random.binomial(size = n, n = 1, p = 1-s)
    
    served, blocked =  simulation(dt, num_steps, m, n, N, T1, T2)
    print(f"Served: {served}, Blocked: {blocked}; proportion blocked: {blocked/(served+blocked)}.\n")
    
    k = s**2 * (s * (-1 + w) - w) * w + c**2 * (-1 + s) * (s**2 * (-1 + w)**2 - s * (-1 + w) * w + w**2) - c * s * (s * (2 - 3 * w) * w + w**2 + s**2 * (1 - 3 * w + 2 * w**2))
    Pb = -(c * (s**2 * (s + w - s * w) + c * (-1 + s) * (s**2 * (-1 + w) - s * w - w**2)))/k
    
    print(f"Theoretical: {Pb}")
    
verify_model_1(1, 1E9, 1, 1, 0.5, 0.4, 0.4)