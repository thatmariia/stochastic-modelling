from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from Simulator import Simulator

params = {
        "l" : 0.5, # lambda
        "s" : 0.3, # mu_s
        "w" : 0.2  # mu_w
}

# setting up the model
model = StochasticModel(params, type=Models.CONTINUOUS)

# calculating transition probs
transition_probabilities = model.get_transition_probabilities(model.matrix)

# setting up simulator
simulator = Simulator(transition_probabilities=transition_probabilities)

# running simulator
simulator.simulate(init_state=States.FF, nr_steps=100)

