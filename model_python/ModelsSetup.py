from enum import Enum, IntEnum
import numpy as np
import csv

class Models(Enum):
    DISCRETE_1 = 0
    DISCRETE_2 = 1
    CONTINUOUS = 2
    TEST = 4

class States(IntEnum):
    FF = 0 #Free Free
    OF = 1 #Occupied Free *if a new customer comes here he will not be surviced 
    FO = 2 #Free Occupied
    OO = 3 #Occupied Occupied *if a new customer comes here he will not be surviced 
    WO = 4 #Waiting Occupied *if a new customer comes here he will not be surviced 


def read_model(filename, d):
    """
    Reads and evaluates matrix from .csv file
    :param filename: string - .csv location
    :param d: map from variables to values
    :return: square probability matrix evaluated with values at d
    """
    filename += ".csv"

    shape = (0,0)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            shape = (shape[0] + 1, shape[1])

            if (len(row) > shape[1]):
                shape = (shape[0], len(row))

    assert shape[0] == shape[1], "The matrix isn't square"

    model_matrix = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            model_row = []
            for cell in row:

                model_cell = eval(cell, d)
                model_row.append(model_cell)
            model_matrix.append(np.array(model_row))

    return np.array(model_matrix)