from StochasticModel import StochasticModel
from ModelsSetup import Models, States
from TransientSimulator import TransientSimulator
from LambdaConstructor import LambdaConstructor
from statistics import mean

def main(l, s, w):
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
                                   t=constructor.t, l=constructor.l, params=params)
    # running simulator
    simulator.simulate(init_state=States.FF)
    return simulator.not_fitting




if __name__ == '__main__':
    best_l = 0.05
    best_s = 0.05
    best_w = 0.05
    min_p = 100.0
    for l in range(40, 100):
        for s in range (5, 40):
            for w in range(5, 40):
                ps = []
                for _ in range(10):
                    p = main (l / 10, s / 10, w / 10)
                    ps.append(p)

                p = mean(ps)
                print (p, l, s, w)
                if p < min_p:
                    min_p = p
                    best_l = l
                    best_s = s
                    best_w = w

    print("BEST")
    print(best_l, best_s, best_w)







