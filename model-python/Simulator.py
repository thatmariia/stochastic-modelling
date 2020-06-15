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
        self.customers_not_fitting(history=history)


    def plot_state_frequency(self, history):
        """
        plots the histogram of all visited states
        :param history: recorded sequence of visited states
        """
        nr_states = len(list(map(int, States)))
        fig, ax = plt.subplots(figsize=(nr_states*4, 16))
        ax.hist(history, bins=nr_states)
        fig.show()

    def customers_not_fitting(self, history):
        state_occurances = [None]*len(list(map(int, States)))
        for j in list(map(int, States)):
            state_occurances[j]=0
            for i in history:
                if i==j:
                    state_occurances[j] = state_occurances[j]+1
        #state_occurances defines the amount of times the system is in given state
        #a customer is not serviced if the system is in state 2,3 or 4
        nr_no_service = state_occurances[2]+state_occurances[3]+state_occurances[4]

        print(self.transition_probabilities)
        percent_no_service = nr_no_service*self.transition_probabilities[0] #FIX TRANSITION PROBABILITY HERE!!!!!!!!
        # print(percent_no_service)


    # FF = 0 #Free Free
    # FO = 1 #Free Occupied
    # OF = 2 #Occupied Free *if a new customer comes here he will not be surviced 
    # OO = 3 #Occupied Occupied *if a new customer comes here he will not be surviced 
    # WO = 4 #Waiting Occupied *if a new customer comes here he will not be surviced 
    # # what is the proportion of customers that do not fit in the store due to a lack of space?