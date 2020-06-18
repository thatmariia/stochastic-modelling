from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from TransientSimulator import TransientSimulator
from LambdaConstructor import LambdaConstructor

params = {
        "l" : 8, # lambda
        "s" : 2,  # mu_s
        "w" : 4   # mu_w
}
nr_steps=30600 # working seconds
is_static = False # whether lambda function is static

def main():
    constructor = LambdaConstructor (max_lambda=params["l"],nr_steps=nr_steps, is_static=is_static)

    # setting up the model
    model = StochasticModel (params, type=Models.CONTINUOUS)

    # setting up simulator
    simulator = TransientSimulator (matrix=model.matrix,
                                    t=constructor.t, l=constructor.l, params=params)
    # running simulator
    simulator.simulate(init_state=States.FF)

if __name__ == '__main__':
    main()






