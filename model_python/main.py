from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from TransientSimulator import TransientSimulator
from LambdaConstructor import LambdaConstructor
from statistics import mean

def simulate(l, s, w, simulating=False):
    params = {
            "l": l,  # lambda
            "s": s,  # mu_s
            "w": w  # mu_w
    }
    nr_steps = 30600  # working seconds
    is_static = False  # whether lambda function is static

    constructor = LambdaConstructor(max_lambda=params["l"], nr_steps=nr_steps, is_static=is_static)

    # setting up the model
    model = StochasticModel(params, type=Models.CONTINUOUS)

    # setting up simulator
    simulator = TransientSimulator(matrix=model.matrix,
                                   t=constructor.t, l=constructor.l, params=params,
                                   simulating=simulating)
    # running simulator
    simulator.simulate(init_state=States.FF)


def get_mean_nofit(epochs, l, s, w):
    ps = [simulate(l, s, w) for _ in range(epochs)]
    return mean(ps)


if __name__ == '__main__':

    l = 9
    s = 3
    w = 6
    epochs = 500
    print("average percentage of non-fitting customers over {} epochs = {}".format(
            epochs, get_mean_nofit(epochs, l, s, w))
    )
    simulate(l, s, w, simulating=True)









