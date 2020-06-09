from ModelsSetup import *

import numpy as np
from scipy.linalg import eig


class StochasticModel:

    def __init__(self, params, type=Models.DISCRETE_1):
        self.params = params
        self.matrix = read_model(type.name, params)

    def get_transition_probabilities(self, generator):
        """
        converting a generator matrix to transtition probability matrix
        :param generator: generator matrix (from the model)
        :return: 2d list
        """
        transition_probabilities = np.zeros(shape=(len(generator), len(generator)))
        for i in range(len(generator)):
            l = abs(generator[i][i])
            for j in range(len(generator)):
                if i == j:
                    transition_probabilities[i][j] = 0
                else:
                    transition_probabilities[i][j] = generator[i][j] / l
        return transition_probabilities

    def get_stationary_distribution_discrete(self):
        """
        Finds stationary distribution for discrete model
        :return: 2d list
        """
        print(self.matrix.T)

        S, U = eig(self.matrix.T)
        try:
            stationary = np.array(U[:, np.where(np.abs(S - 1.) < 1e-8)[0][0]])
            return stationary / np.sum(stationary)
        except:
            print("Can't find stationary distribution")
            return -1
