import sys
import os.path
import numpy as np
import pandas as pd

# create a method for calculating score
def getOutputEstimate(row, weights):
    return (weights[0] * row['x0']) + (row['x1'] * weights[1]) + (row['x2'] * weights[2])

# create a method for easy line plotting
def createLinePlots(df, weights):
    result = []
    for i in range(len(df)):
        result.append(weights[0] + (i * weights[1]) + (i * weights[2]))

    return result

# tells if the current weighs classify point correctly
def isClassifiedCorrectly(row, weights):
    return (row['value'] * getOutputEstimate(row, weights)) > 0

#determines the new weights by adding errors
def updateWeights(df, weights):
    for i, row in df.iterrows():
        if not isClassifiedCorrectly(row, weights):
            #print('incorrect classifier', row['x'], row['y'], row['value'])
            for i in range(len(weights)):
                df_map = ['x0', 'x1', 'x2']
                weights[i] += (row[df_map[i]]*row['value'])

    return weights

#create helper function for determing convergence
def converged(df, weights):
    for i, row in df.iterrows():
        if not isClassifiedCorrectly(row, weights):
           return False

    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <input csv> <output file>")
        sys.exit()

    if  not os.path.isfile(sys.argv[1]) or sys.argv[1][-4:] != '.csv':
        print("Usage: {} <input csv> <output file>")
        sys.exit()

    # create df
    df = pd.read_csv('input1.csv', header=None, names=['x1', 'x2', 'value'], sep=',', error_bad_lines=False)
    df['color'] = np.where(df['value'] == 1, 'blue', 'red')
    df['x0'] = 1 # to always multiply by bias

    # initialize weights = 0 to start
    weights = np.zeros(3)
    converge_complete = converged(df, weights)
    output_file = open(sys.argv[2], 'w')

    while (not converge_complete):
        converge_complete = converged(df, weights)
        updateWeights(df, weights)
        output_file.write(str(weights[1]) + ',' + str(weights[2]) + ',' + str(weights[0]) + "\n")

    output_file.close()
