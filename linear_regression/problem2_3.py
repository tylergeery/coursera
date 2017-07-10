import sys
import os.path
import numpy as np
import pandas as pd

def output(filename):
    output_file = open(filename, 'w')

    while (not converge_complete):
        converge_complete = converged(df, weights)
        updateWeights(df, weights)
        output_file.write(str(weights[1]) + ',' + str(weights[2]) + ',' + str(weights[0]) + "\n")

    output_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    if  not os.path.isfile(sys.argv[1]) or sys.argv[1][-4:] != '.csv':
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    # create df
    df = pd.read_csv(sys.argv[1], header=None, names=['age', 'weight', 'height'], sep=',', error_bad_lines=False)
    df['color'] = np.where(df['value'] == 1, 'blue', 'red')
    df['x0'] = 1 # to always multiply by bias

    # initialize weights = 0 to start
    weights = np.zeros(3)
    converge_complete = converged(df, weights)

    output(sys.argv[2])
