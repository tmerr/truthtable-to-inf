"""
Prompts the user for a truth table then generates sentences in implicative normal
form (INF) that match it.
"""


import itertools
import string
import math


def powerset(seq):
    """Return all subsets of this set."""
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item


def evaluate_sentence(sentence, assignments):
    """
    Calculate the truth value of the given sentence and variable assignments.

    Params
        sentence: the combination of INF form implications. For example
                  "(a, c => b)^(c, b => d)" would be (((0, 2),(1)), ((2, 1),(3)))
        assignments: a: T, b: F, c: T would be (True, False, True).

    Return
        Whether the sentence is True or False.
    """
    for and_idxs, or_idxs in sentence:
        # substitute in truth values so we have something like  "T ^ T ^ F => F ^ T
        and_values = (assignments[i] for i in and_idxs)
        or_values = (assignments[j] for j in or_idxs)

        # simplify it to an implication T => T
        ands_true = all(and_values)
        ors_true = any(or_values)

        # evaluate the implication
        implication_truth = (not ands_true) or ors_true
        
        # short circuit AND together the truths of the implications
        if implication_truth == False:
            return False

    return True


def find_inf_sentences(truth_table, implication_count):
    """
    Generate sentences in INF form that produce the output specified in the truth table.
    Often the truth table can't be represented by a single implication, hence the
    implication count parameter.
    """
    num_vars = math.log(len(truth_table), 2)
    if num_vars.is_integer():
        num_vars = int(num_vars)
    else:
        raise ValueError('Invalid size for truth table.')

    # implications are in the form
    # a_1 ^ ... ^ a_n => b_1 v ... v b_n
    implication_possibilities = itertools.product(powerset(list(range(num_vars))), repeat=2)

    # we should have a large list of [(imp1 ^ imp2 ^ ... impN), ...]
    sentences = itertools.product(implication_possibilities, repeat=implication_count)

    # we want to find sentences that agree with the truth table for every set of assignments
    for sentence in sentences:
        same = (evaluate_sentence(sentence, assignments) == output for (assignments, output) in truth_table)
        if all(same):
            yield sentence


def build_truth_table():
    """
    Build truth table in the form [((True, True, True), True), ((True, True, False), False), ... ]
    The user is prompted for the values.
    """
    while True:
        try:
            num_vars = int(input('Number of variables: '))
            break
        except ValueError:
            print('Must be an integer.')

    print('\nComplete the following truth table.\n')
    print(' '.join(string.ascii_lowercase[:num_vars]))
    truth_table = []
    for assignment in itertools.product([True, False], repeat=num_vars):
        truthiness = None
        while truthiness is None:
            truefalses = ' '.join(['T' if v else 'F' for v in assignment])
            result = input('{} -> '.format(truefalses))
            if result == 'T':
                truthiness = True
            elif result == 'F':
                truthiness = False
            else:
                print('Enter T/F')
        truth_table.append((assignment, truthiness))
    
    return truth_table


def run():
    """
    Run the program.
    """
    table = build_truth_table()

    for implication_count in itertools.count(1):
        for sentence in find_inf_sentences(table, implication_count):
            total = []
            for (and_idxs, or_idxs) in sentence:
                and_symbols = [string.ascii_lowercase[i] for i in and_idxs]
                or_symbols = [string.ascii_lowercase[j] for j in or_idxs]
                text = '({} => {})'.format(' ^ '.join(['T'] + and_symbols), ' v '.join(or_symbols + ['F']))
                total.append(text)
            print(' ^ '.join(total))
        inp = input('Order {} done. enter: more. q: quit. '.format(implication_count))
        if inp == 'q':
            return
    

if __name__ == '__main__':
    run()
