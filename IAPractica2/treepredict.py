#! /usr/bin/env python2
# -*- coding: utf-8 -*-

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0
    def size(self):
        "Returns the queue's size"
        return len(self.list)
    def print_(self):
        print "------ I -------"
        for e in self.list:
            print e
        print "------ O -------"

    def print_size(self):
        print (self.size())


# --------------------- t1  ---------------------
# Download the data file descision_tree_example.txt from the virtual campus at folder/lab/learning.
# --------------------- t2  ---------------------
# Create a file named treepredict.py.
# --------------------- t3  ---------------------
# Define a function to load the data into a bidimensional list named data.
def read_file(file_path, data_sep=",", ignore_first_line=False):
    prototypes = []
    # Open file
    with open(file_path, "r") as fh:
        # Strip lines
        strip_reader = (line.strip() for line in fh)

        # Filter empty lines
        filtered_reader = (line for line in strip_reader if line)

        # Skip first line if needed
        if ignore_first_line:
            next(filtered_reader)

        # Split lines, parse token and append to prototypes
        for line in filtered_reader:
            prototypes.append(
                [filter_token(token) for token in line.split(data_sep)]
            )

    return prototypes


def filter_token(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


# --------------------- t4  ---------------------
# Define a function unique_counts that counts the number of prototypes of a given class in a partition part.
# Create counts of possible results
# (the last column of each row is the result).
def unique_counts(part):
    # import collections
    # return dict(collections.Counter(row[-1] for row in part)
    results = {}
    for row in part:
        results[row[-1]] = results.get(row[-1], 0) + 1
    #    if row[-1] not in results.keys():
    #        results[row[-1]] = 1
    #    else:
    #        results[row[-1]] += 1

    return results


# --------------------- t5  ---------------------
# Define a function that computes the Gini index of a node.
def gini_impurity(part):
    total = float(len(part))
    results = unique_counts(part)

    return 1 - sum((count / total) ** 2 for count in results.values())


# --------------------- t6  ---------------------
# Define a function that computes the entropy of a node.
def entropy(part):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = unique_counts(part)
    # Now calculate the entropy
    total = float(len(part))
    return -sum(
        (count / total) * log2(count / total) for count in results.values()
    )


# --------------------- t7  ---------------------
#  Define a function that partitions a previous partition, taking
# into account the values of a given attribute (column).
def divideset(part, column, value):
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] <= value
    else:
        split_function = lambda row: row[column] == value
    # Split "part accordinf "split_function"
    set1 = [row for row in part if split_function(row)]
    set2 = [row for row in part if not split_function(row)]
    return set1, set2


# --------------------- t8  ---------------------
# Define a new class decisionnode, which represents a node in the tree.
class desicionnode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


# --------------------- t9  ---------------------
# Construcción del árbol de forma recursiva.
def buildtree(dataset, score_func=gini_impurity, beta=0):
    if len(dataset) == 0:
        return desicionnode()
    impurity = score_func(dataset)

    # best split criteria
    best_impurity_decrease, criteria, sets = split_dataset(dataset, impurity, score_func)

    if best_impurity_decrease > beta:
        return desicionnode(col=criteria[0], value=criteria[1], tb=buildtree(sets[0]), fb=buildtree(sets[1]))
    else:
        return desicionnode(results=unique_counts(dataset))


def split_dataset(dataset, impurity, score_func):
    """splits data set in two sets"""
    best_decrease_impurity = 0
    criteria = None
    sets = None
    for atribute_idx in range(len(dataset[0]) - 1):
        atribute_values = get_column_values(atribute_idx, dataset)
        for value in atribute_values:
            (setT, setF) = divideset(dataset, atribute_idx, value)
            impurityT = score_func(setT)
            impurityF = score_func(setF)
            impurity_decrease = impurity - ((float(len(setT)) / len(dataset)) * impurityT) - (
                        (float(len(setF)) / len(dataset)) * impurityF)

            if len(setT) > 0 and len(setF) > 0 and impurity_decrease > best_decrease_impurity:
                best_decrease_impurity = impurity_decrease
                criteria = (atribute_idx, value)
                sets = (setT, setF)
    return best_decrease_impurity, criteria, sets


def get_column_values(atribute_idx, dataset):
    atribute_values = []
    for row in dataset:
        if row not in atribute_values:
            atribute_values.append(row[atribute_idx])
    return atribute_values


# --------------------- t10 ---------------------
# Construcción del árbol de forma iterativa.
def buildtree_iterative(dataset, score_func=gini_impurity, beta=0):
    print " ---------------------  BEGIN PREVIEW  --------------------- "
    if len(dataset) == 0:
        return desicionnode()


    q = Queue()
    q.print_()
    q.push((dataset,False))
    q.print_()
    print "inici bucle"

    while not q.isEmpty():

        part, leaf = q.pop()
        q.print_()
        print "-->", part

        if not leaf:
            best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
            if best_impurity_decrease > beta:
                print "------------ criteria ", criteria[1], " -----------------"
                print "set extracted:    "+str(criteria[1])
                print "set extracted: No " + str(criteria[1])
                q.push((sets[0], False))
                q.push((sets[1], False))
            else:
                q.push((unique_counts(part), True))
        else:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"+str(part)
            pass
        print "##########################################################################"
    print " --------------------- EBD PREVIEW --------------------- "






    '''


    q.print_()
    print "inici bucle"
    part = q.pop()
    print "-->",part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"



    q.print_()
    part = q.pop()
    print "-->", part
    best_impurity_decrease, criteria, sets = split_dataset(part, score_func(part), score_func)
    if best_impurity_decrease > beta:
        print "------------", criteria[1], " -----------------"
        q.push(sets[0])
        q.push(sets[1])
    else:
        print "---------------- BETA !!---------------"
        q.push(unique_counts(part))
    print "##########################################################################"
    '''











# --------------------- t11 ---------------------
# Include the following function printtree:
def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results is not None:
        print(indent + str(tree.results))
    else:
        # Print the criteria
        print(indent + str(tree.col) + ':' + str(tree.value) + '? ')
        # Print the branches
        print(indent + 'T->')
        printtree(tree.tb, indent + '  ')
        print(indent + 'F->')
        printtree(tree.fb, indent + '  ')


# --------------------- t12 ---------------------
# Función de clasificación.
# --------------------- t13 ---------------------

if __name__ == '__main__':
    prototypes = read_file("decision_tree_example.txt", data_sep=",", ignore_first_line=True)
    count = unique_counts(prototypes)
    giniIndex = gini_impurity(prototypes)
    entropyValue = entropy(prototypes)
    #print"\nGini Index: " + str(giniIndex) + " Entropy: " + str(entropyValue)
    buildtree_iterative(prototypes)
    desisicion_tree = buildtree(prototypes)

    printtree(desisicion_tree)


    #printtree(desisicion_tree)

    # print unique_counts(prototypes)
    # print gini_impurity(prototypes)
    # print entropy(prototypes)
    # set1,set2= divideset(prototypes,column=0,value="google")
    # print set1
    # print
    # print set2
    pass
