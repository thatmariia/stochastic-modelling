import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from ModelsSetup import *
import collections
from statistics import mean


class TransientSimulator:

    def __init__(self, matrix, t, l, params):
        self.generator_matrix = matrix

        self.t = t
        self.l = l
        self.params = params

        self.not_fitting = 0.0

    def recalculate_matrix(self, t):
        """
        calculates the transition matrix based on the time
        :param t: current time
        :return: 2d list transition probs
        """
        self.params["l"] = self.l[self.t==t][0]
        self.generator_matrix = read_model(Models.CONTINUOUS.name, self.params)


    def get_next_step(self, curr_state_nr):
        """
        Gets the next step based on generator matrix
        :param curr_state_nr:
        :return: min rate and the corresponding state
        """
        min_sample = np.inf
        next_state_nr = curr_state_nr

        examined_state_nr = 0
        for hourly_rate in self.generator_matrix[curr_state_nr]:
            rate = hourly_rate / 3600 # to match seconds iteration

            if rate != 0 and examined_state_nr != curr_state_nr:
                sample = np.random.exponential(scale=1/rate)
                if sample < min_sample:
                    min_sample = int(round(sample))
                    next_state_nr = examined_state_nr
            examined_state_nr += 1

        return min_sample, next_state_nr

    def simulate(self, init_state: States):
        """
        Monte carlo simulation
        :param init_state: starting state
        """
        history = [init_state]
        init_state_nr = init_state.value

        # Going around the chain for nr_steps
        for i in range(len(self.t)):
            self.recalculate_matrix(t=self.t[i])

            # determining next state and associated rate
            rate, next_step_nr = self.get_next_step(curr_state_nr=init_state_nr)

            #print("sitting in state {} for {} seconds".format(init_state.name, rate))

            # quit if the simulation finishes by the time we transition
            if len(history) + rate > len(self.t):
                history += [States(next_step_nr)] * (len(self.t) - len(history))
                break

            # waiting in the current state for 'rate' steps
            i += rate

            # adding the waiting in curr state history to overall hitory
            history += [init_state] * rate

            # finally transitioning to the next step
            init_state = States(next_step_nr)
            init_state_nr = next_step_nr

        #print(history)

        # Plotting visiting frequency
        #self.plot_state_frequency(history=history)
        self.not_fitting = self.customers_not_fitting(history=history)

    def plot_state_frequency(self, history):
        """
        plots the histogram of all visited states
        :param history: recorded sequence of visited states
        """
        nr_states = len(list(map(int, States)))
        size=25

        colors = ["#264653", "#e76f51", "#2a9d8f", "#e9c46a", "#f4a261"]

        plot_params = {
                      'legend.fontsize': 'large',
                      'figure.figsize' : (20,8),
                      'axes.labelsize' : size,
                      'axes.titlesize' : size,
                      'xtick.labelsize': size*0.85,
                      'ytick.labelsize': size*0.85,
                      'axes.titlepad'  : 25
        }
        plt.rcParams.update(plot_params)
        fig, ax = plt.subplots(2, figsize=(nr_states*4, 20))


        # lambda function
        ax[0].set_title("Change of lambda with time", fontsize=50)
        ax[0].plot(np.linspace(10, 19, 13),
                   np.full(13, fill_value=mean(self.l)),
                   color=colors[2], linestyle=":", linewidth=7,
                   label="mean")
        ax[0].plot (self.t, self.l, color=colors[1], linewidth=10,
                    label="values")
        ax[0].legend(loc=2, fontsize=20)
        ax[0].set_ylabel("lambda", size=40)
        ax[0].set_xlabel ("hour of the day", size=40)
        ax[0].set_xlim([10, 18.5])

        ax[0].text(
                10.3, mean(self.l),
                "{}".format(round(mean(self.l), 2)),
                fontsize=40, color=colors[2],
                ha="left", va="bottom"
        )

        # state visiting frequency
        frequencies = collections.Counter(history)
        ax[1].set_title("State visiting frequency", fontsize=50)
        ax[1].bar(frequencies.keys(), frequencies.values(), width=0.3, color=colors)
        plt.xticks(np.arange(len(frequencies)), frequencies.keys())
        ax[1].set_ylabel("seconds spent", size=40)
        ax[1].set_xlabel ("states", size=40)

        not_fitting = round(self.customers_not_fitting(history),2)
        ax[1].text(
                len(frequencies)-1, max(frequencies.values()),
                "no fit\n{}%".format(not_fitting),
                fontsize=40, color=colors[2],
                ha="center", va="top",
                bbox=dict(facecolor=colors[3], alpha=0.5)
        )

        fig.show()

    def customers_not_fitting(self, history):
        """
        calculates the percentage of customers that didnt fit
        :param history: recorded sequence of visited states
        :return: percentage float [0.0, 100.0]
        """
        frequencies = collections.Counter(history)
        if not States.OO in frequencies:
            frequencies[States.OO] = 0
        if not States.WO in frequencies:
            frequencies[States.WO] = 0
        if not States.OF in frequencies:
            frequencies[States.OF] = 0

        all_freqs = float(sum([freq for freq in frequencies.values()]))
        occupied_freqs = float(frequencies[States.OO] + frequencies[States.WO] + frequencies[States.OF])
        return 100.0 * (occupied_freqs / all_freqs)



    """
        FF = 0 #Free Free
        OF = 1 #Occupied Free *if a new customer comes here he will not be surviced 
        FO = 2 #Free Occupied
        OO = 3 #Occupied Occupied *if a new customer comes here he will not be surviced 
        WO = 4 #Waiting Occupied *if a new customer comes here he will not be surviced 
    """