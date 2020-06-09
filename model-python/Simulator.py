import numpy as np
import matplotlib.pyplot as plt
from ModelsSetup import States

class Simulator:

    def __init__(self, transition_probabilities):
        self.transition_probabilities = transition_probabilities

    def simulate(self, init_state: States, nr_steps):
        history = [init_state]
        init_state_nr = init_state.value

        # Going around the chain for nr_steps
        for i in range(nr_steps):
            next_step_nr = np.random.choice(a=list(map(int, States)),
                                            size=1,
                                            p=self.transition_probabilities[init_state_nr])[0]

            history.append(States(next_step_nr))
            init_state_nr = next_step_nr
        print(history)

        # Plotting visiting frequency
        self.plot_state_frequency(history=history)



    def plot_state_frequency(self, history):
        """
        plots the histogram of all visited states
        :param history: recorded sequence of visited states
        """
        nr_states = len(list(map(int, States)))
        fig, ax = plt.subplots(figsize=(nr_states*4, 16))
        ax.hist(history, bins=nr_states)
        fig.show()