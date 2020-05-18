from ModelsSetup import *

import numpy as np
from scipy.linalg import eig


class StochasticModel:

    def __init__(self, params, type=Models.DISCRETE_1):
        self.states = States
        self.params = params

        self.transition_probabilities = read_model (type.name, params)

    def set_model(self, model):
        self.model = model

    def get_stationary_distribution(self):
        print(self.transition_probabilities.T)

        S, U = eig(self.transition_probabilities.T)
        try:
            stationary = np.array(U[:, np.where(np.abs(S - 1.) < 1e-8)[0][0]])
            return stationary / np.sum(stationary)
        except:
            print("Can't find stationary distribution")
            return -1
