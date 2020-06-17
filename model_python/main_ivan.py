from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from Simulator import Simulator
from TransientSimulator import TransientSimulator
from LambdaConstructor import LambdaConstructor
import numpy as np
# from <MySubFolder> import <MyFile>

params = {
        "l" : 0.5, # lambda
        "s" : 0.3, # mu_s   
        "w" : 0.2  # mu_w
}

"""
Define lambda that is changing with time 
Assumptioms:
    * working hours from 10-18:30
"""
#define time vector
nr_steps=9000
constructor = LambdaConstructor(nr_steps=nr_steps, is_static=False)


# setting up the model
#model.matrix -> transition probabilities
model = StochasticModel(params, type=Models.DISCRETE_1)

# setting up simulator
simulator = TransientSimulator(t = constructor.t, l = constructor.l, params = params)

# running simulator
simulator.simulate(init_state=States.FF)

#static simulator
simulator_static = Simulator(transition_probabilities=model.matrix)
simulator_static.simulate(init_state=States.FF, nr_steps=9000)

# generatate stationary distribution

