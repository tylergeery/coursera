import sys
import os.path
import math
import numpy as np
import pandas as pd

def output(filename, results):
    output_file = open(filename, 'w')

    for result in results:
        values = [result['alpha'], result['iters'], result['weights'][0], result['weights'][1], result['weights'][2]]
        str_values = [str(val) for val in values]
        output_file.write(','.join(str_values) + "\n")

    output_file.close()

def stats(series):
    sm = 0
    mn = series.sum()/series.count()
    for i, value in series.iteritems():
        sm += math.pow(value - mn, 2)

    return mn, (math.sqrt(sm/series.count()))

# def linear model
def linear_model(weights, features):
    return sum([weights[i] * features[i] for i in range(len(weights))])

def run(df):
    results = []

    #get the std dev for a series
    mn_age, std_dev_age = stats(df['age'])
    mn_weight, std_dev_weight = stats(df['weight'])

    df['age_scaled'] = (df['age'] - mn_age)/std_dev_age
    df['weight_scaled'] = (df['weight'] - mn_weight)/std_dev_weight

    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, .08]
    weight_map = ['bias', 'age_scaled', 'weight_scaled']
    obs_divisor = 1/(len(df))

    for alpha in alphas:
        iters = i = 100 #iterations
        weights = np.zeros(3) #initialize weights to 0
        scalar = alpha * obs_divisor

        while (i > 0):
            i -= 1
            linear_model = lambda row: np.dot(weights, [row[c] for c in ['bias', 'age_scaled', 'weight_scaled']])
            df['est'] = df.apply(linear_model, 1)

            for beta_index in range(len(weights)):
                weights[beta_index] -= (scalar * ((df['est'] - df['height']) * df[weight_map[beta_index]]).sum())

        results.append({
            'alpha': alpha,
            'iters': iters,
            'weights': weights
        })

    return results

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    if  not os.path.isfile(sys.argv[1]) or sys.argv[1][-4:] != '.csv':
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    # create df
    df = pd.read_csv(sys.argv[1], header=None, names=['age', 'weight', 'height'], sep=',', error_bad_lines=False)
    df['bias'] = 1 # to always multiply by bias

    results = run(df)

    output(sys.argv[2], results)
