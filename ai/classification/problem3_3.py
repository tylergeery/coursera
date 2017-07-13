import sys
import os.path
import math
import numpy as np
import pandas as pd
from sklearn import neighbors, datasets, svm, linear_model, neighbors, tree, ensemble
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, GridSearchCV

class Process:
    def __init__(self, df, output_filename):
        X_train, X_test, y_train, y_test = train_test_split(df[['x1', 'x2']], df['value'], test_size=0.4, random_state=0, stratify=df['value'])
        X, Y = np.meshgrid(X_train['x1'], X_train['x2'])

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.X = X
        self.Y = Y
        self.output_filename = output_filename
        self.results = []

    def output(self):
        """
        Outputs a file to filename

        This file will contain the results of the 7 classifier attempts
        in csv format

        e.g svm_linear, 0.2567, 45.76
        """
        output_file = open(self.output_filename, 'w')

        for values in self.results:
            str_values = [str(val) for val in values]
            output_file.write(','.join(str_values) + "\n")

        output_file.close()

    def fit_model(self, model_name, classifier, parameters):
        """
        Fit a given classifier using sklearn grid_search and a cv of 5

        Returns: [model_name, best_score, test_score]
        """
        clf = GridSearchCV(classifier, parameters, cv=5)
        clf.fit(self.X_train[['x1', 'x2']], self.y_train)

        best_score = max(clf.cv_results_['mean_train_score'])
        test_score = clf.score(self.X_test, self.y_test)

        return [model_name, best_score, test_score]

    def run(self):
        """
        Runs the 7 different classifiers and returns results of the run on the dataset
        """
        # define parameters
        svm_linear_params = {'kernel':['linear'], 'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
        svm_poly_params = {'kernel':['poly'], 'C':[0.1, 1, 3], 'degree':[4,5,6], 'gamma':[0.1,0.5]}
        svm_rbf_params = {'kernel':['rbf'], 'C':[0.1, 0.5, 1, 5, 10, 50, 100], 'gamma':[0.1, 0.5, 1, 3, 6, 10]}
        logistic_params = {'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
        knn_params = {'n_neighbors': range(1, 51), 'leaf_size': range(5, 61, 5)}
        dt_params = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
        rf_params = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}

        self.results.append(self.fit_model('svm_linear', svm.SVC(), svm_linear_params))
        self.results.append(self.fit_model('svm_polynomial', svm.SVC(), svm_poly_params))
        self.results.append(self.fit_model('svm_rbf', svm.SVC(), svm_rbf_params))
        self.results.append(self.fit_model('logistic', linear_model.LogisticRegression(), logistic_params))
        self.results.append(self.fit_model('knn', neighbors.KNeighborsClassifier(), knn_params))
        self.results.append(self.fit_model('decision_tree', tree.DecisionTreeClassifier(), dt_params))
        self.results.append(self.fit_model('random_forest', ensemble.RandomForestClassifier(), rf_params))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    if  not os.path.isfile(sys.argv[1]) or sys.argv[1][-4:] != '.csv':
        print("Usage: {} <input csv> <output file>".format(sys.argv[0]))
        sys.exit()

    # create df
    df = pd.read_csv(sys.argv[1], header=0, names=['x1', 'x2', 'value'], sep=',', error_bad_lines=False)

    # run the program
    proc = Process(df, sys.argv[2])
    proc.run()
    proc.output()
