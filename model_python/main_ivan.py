from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from Simulator import Simulator
from TransientSimulator import TransientSimulator
import numpy as np
# from <MySubFolder> import <MyFile>

params = {
        "l" : 0.5, # lambda
        "s" : 0.3, # mu_s   
        "w" : 0.2  # mu_w
}

#now define lambda that is changing with time 
#assumptions: 
#working hours from 10-18:30
#define time vector
nr_steps=9000
t =  np.linspace(10.0, 19.0, nr_steps)
#define lambda as a function of time 
l = np.array([0.0]*nr_steps)
l[t<13] = (0.1+0.05*(t[t<13]-10)) # probability starts at 0.1 and increases to 0.25
l[(t>=13) & (t<16)]=0.25-0.1/3*(t[(t>=13) & (t<16)]-13) # probability starts at 0.25 at 13:00 and falls to 0.15 at 16:00
l[(t>=16) & (t<18)]=0.15+0.45/2*(t[(t>=16) & (t<18)]-16)# probability starts at 0.15 at 16:00 and increases to 0.6 at 18:00
l[t>=18]=0.6# probability stays at 0.6 until the end


# setting up the model
#model.matrix -> transition probabilities
model = StochasticModel(params, type=Models.DISCRETE_1)

# setting up simulator
simulator = TransientSimulator(t = t, l = l, params = params)

# running simulator
simulator.simulate(init_state=States.FF, nr_steps=100)



# generatate stationary distribution

