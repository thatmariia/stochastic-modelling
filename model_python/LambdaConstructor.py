import numpy as np

class LambdaConstructor:

    def __init__(self, nr_steps, is_static=True):
        """
        Define lambda as a function of time
        :param nr_steps: length of training
        :param is_static: whether lambda is changing with time
        """
        self.t = np.linspace(10.0, 19.0, nr_steps)

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

        # probability starts at 0.1 and increases to 0.25
        self.l[self.t < 13] = (0.1 + 0.05 * (self.t[self.t < 13] - 10))

        # probability starts at 0.25 at 13:00 and falls to 0.15 at 16:00
        self.l[(self.t >= 13) & (self.t < 16)] = 0.25 - 0.1 / 3 * (
                self.t[(self.t >= 13) & (self.t < 16)] - 13)

        # probability starts at 0.15 at 16:00 and increases to 0.6 at 18:00
        self.l[(self.t >= 16) & (self.t < 18)] = 0.15 + 0.45 / 2 * (
                self.t[(self.t >= 16) & (self.t < 18)] - 16)

        # probability stays at 0.6 until the end
        self.l[self.t >= 18] = 0.6