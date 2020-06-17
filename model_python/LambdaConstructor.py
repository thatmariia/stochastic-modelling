import numpy as np
from math import exp
class LambdaConstructor:

    def __init__(self, max_lambda, nr_steps, is_static=True):
        """
        Define lambda as a function of time
        :param nr_steps: length of training
        :param is_static: whether lambda is changing with time
        """
        self.t = np.linspace(10.0, 19.0, nr_steps)
        self.max_lambda = max_lambda

        if is_static:
            self._generate_static(nr_steps)
        else:
            self._generate_changing(nr_steps)

    # TODO:: pass values

    def _generate_static(self, nr_steps):
        self.l = np.array ([0.6] * nr_steps)

    def _generate_changing(self, nr_steps):
        """
        Define lambda that is changing with time
        Assumptioms:
            * working hours from 10-18:30
        """
        self.l = np.array ([0.0] * nr_steps)

        for i in range(nr_steps):
            if self.t[i] <= 16:
                mid = 13
                self.l[i] = self.max_lambda/8 + (3*self.max_lambda/8) / (1+(self.t[i]-mid)**2)
            else:
                mid = 17.25
                touch = self.l[0]
                self.l[i] = (self.max_lambda-touch)/2 * (np.tanh((self.t[i]-mid)*2.6)+1) + touch

