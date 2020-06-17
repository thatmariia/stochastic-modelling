from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from Simulator import Simulator
from TransientSimulator import TransientSimulator
from LambdaConstructor import LambdaConstructor

params = {
        "l" : 20, # lambda
        "s" : 8, # mu_s
        "w" : 3  # mu_w
}
nr_steps=30600 # working seconds
is_static = False # whether lambda function is static

def static():
    # setting up the model
    model = StochasticModel(params, type=Models.CONTINUOUS)

    # calculating transition probs
    transition_probabilities = model.get_transition_probabilities(model.matrix)

    # setting up simulator
    simulator = Simulator(transition_probabilities=transition_probabilities)

    # running simulator
    simulator.simulate(init_state=States.FF, nr_steps=nr_steps)


def not_static():
    constructor = LambdaConstructor (max_lambda=params["l"],nr_steps=nr_steps, is_static=is_static)

    # setting up the model
    model = StochasticModel (params, type=Models.CONTINUOUS)
    print(model.matrix)

    # setting up simulator
    simulator = TransientSimulator (matrix=model.matrix,
                                    t=constructor.t, l=constructor.l, params=params)

    # running simulator
    simulator.simulate(init_state=States.FF)

    # static simulator
    #simulator_static = Simulator (transition_probabilities=model.matrix)
    #simulator_static.simulate (init_state=States.FF, nr_steps=nr_steps)




if __name__ == '__main__':

    if is_static:
        static()
    else:
        not_static()





