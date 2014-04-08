#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        value = int(parts[0])
        weight = int(parts[1])
        density = float(value)/float(weight)
        print density
        items.append(Item(i-1, value, weight, density))

    # outer variable controls (indexes)
    value = 0
    weight = 0
    taken = [0]*len(items)
    max = 0

    # sort the list of tuples by density so that a new possible max
    # can be guaranteed to be the best available as we iterate through
    items = sorted(items, key=lambda x: x.density, reverse=True)

    print items

    # We will refer to a new "bag" with each iteration through items
    # the bag variable will be compared to the global maxes at end
    # of each iteration
    for i in items:
        bag_value = 0
        bag_weight = 0
        bag_taken = [0]*len(items)
        bag_max = 0

        # Only start adding in the items after the next one up
        # so that we are not trying arrangements that are repeating themselves
        for j in xrange(i, len(items)):
            item = items[j]


            # Create a new max weight to see if passing this node
            # is even necessary

            hopeful = bag_value + item.value * (capacity - bag_weight) / item.weight


            # If the new max weight is not larger than our existing best,
            # then we can exit this current loop and try again with
            # a new starting item
            # And of course if it is larger
            if hopeful < max:
                break
            else:
                max = i_max

            # Here is where items are actually added to the current bag
            # Need to increment current bag.. value, weight
            if bag_weight + item.weight <= capacity:
                bag_taken[item.index] = 1
                bag_value += item.value
                bag_weight += item.weight

            # If the bag has reached capacity, we should stop iterating on this bag
            if bag_weight == capacity:
                break

        # Now save the values that are new optimums
        if bag_max > max:
            max = bag_max


    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    if len(sys.argv) > 0:
        # file_location = sys.argv[1].strip()
        file_location = 'data/ks_4_0'
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

