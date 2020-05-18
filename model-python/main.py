from StochasticModel import *

params = {
        "c" : 1,
        "s" : 1,
        "w" : 1
}

model = StochasticModel(params)
print(model.get_stationary_distribution())