import numpy as np
import matplotlib.pyplot as plt
from ModelsSetup import *



class TransientSimulator:

    def __init__(self, t, l, params):
        # self.transition_probabilities
        self.t = t
        self.l = l
        self.params = params

    def get_transition_matrix(self, t):
        '''
            calculates the transition matrix based on the time 
        '''
        l = self.l[self.t==t][0]
        self.params["l"] = l
        self.transition_probabilities = read_model("DISCRETE_1", self.params)

    def simulate(self, init_state: States):
        history = [init_state]
        init_state_nr = init_state.value

        # Going around the chain for nr_steps
        for i in self.t:
            self.get_transition_matrix(t=i)
            # print(self.transition_probabilities)
            next_step_nr = np.random.choice(a=list(map(int, States)),
                                            size=1,
                                            p=self.transition_probabilities[init_state_nr])[0]

            history.append(States(next_step_nr))
            init_state_nr = next_step_nr
        print(history)

        # Plotting visiting frequency
        self.plot_state_frequency(history=history)
        self.customers_not_fitting(history=history, nr_steps=len(self.t))


    def plot_state_frequency(self, history):
        """
        plots the histogram of all visited states
        :param history: recorded sequence of visited states
        """
        nr_states = len(list(map(int, States)))
        size=25
        # size=15
        plot_params = {'legend.fontsize': 'large',
          'figure.figsize': (20,8),
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75,
          'axes.titlepad': 25}
        plt.rcParams.update(plot_params)
        fig, ax = plt.subplots(2, figsize=(nr_states*4, 16))
        # fig, ax = plt.subplots(figsize=(2))
        ax[0].plot(self.t, self.l)
        ax[1].hist(history, bins=nr_states)
        fig.show()

    def customers_not_fitting(self, history, nr_steps):
        state_occurances = [None]*len(list(map(int, States)))
        for j in list(map(int, States)):
            state_occurances[j]=0
            for i in history:
                if i==j:
                    state_occurances[j] = state_occurances[j]+1
        #state_occurances defines the amount of times the system is in given state
        #a customer is not serviced if the system is in state 2,3 or 4
        nr_no_service = state_occurances[2]+state_occurances[3]+state_occurances[4]

        # print(self.transition_probabilities)
        percent_no_service = nr_no_service/nr_steps*self.transition_probabilities[0][2] 
        print("\nThe percent of cutomers that will not fit is: ")
        print(percent_no_service)
        print("\n")
        print(self.transition_probabilities)



    #   FF = 0 #Free Free
    # OF = 1 #Occupied Free *if a new customer comes here he will not be surviced 
    # FO = 2 #Free Occupied
    # OO = 3 #Occupied Occupied *if a new customer comes here he will not be surviced 
    # WO = 4 #Waiting Occupied *if a new customer comes here he will not be surviced 