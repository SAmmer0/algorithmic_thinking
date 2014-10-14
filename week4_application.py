# -*- coding: utf-8 -*-
"""
Code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import week4_project as student
else:
    import simpleplot
    import userXX_XXXXXXX as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code
def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def question1():
    '''
    Solver program for question 1
    '''
    human = read_protein(HUMAN_EYELESS_URL)
    fruit_fly = read_protein(FRUITFLY_EYELESS_URL)
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    alignment_matrix = student.compute_alignment_matrix(human, fruit_fly,
                                                        scoring_matrix,
                                                        False)
    alignment = student.compute_local_alignment(human, fruit_fly,
                                                scoring_matrix,
                                                alignment_matrix)
    # with open('question1_result.txt', 'w') as f:
    #     f.write('Score:' + str(alignment[0]) + '\n')
    #     f.write('Human:' + str(alignment[1]) + '\n')
    #     f.write('Fruit fly:' + str(alignment[2]) + '\n')
    print 'Score:', alignment[0]
    print 'Human:', alignment[1]
    print 'Fruit fly:', alignment[2]


def question2():
    '''
    Solution for question 2
    '''
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    pax = read_protein(CONSENSUS_PAX_URL)
    human = read_protein(HUMAN_EYELESS_URL)
    fruit_fly = read_protein(FRUITFLY_EYELESS_URL)
    alignment_matrix_hf = student.compute_alignment_matrix(human, fruit_fly,
                                                           scoring_matrix,
                                                           False)
    alignment_hf = student.compute_local_alignment(human, fruit_fly,
                                                   scoring_matrix,
                                                   alignment_matrix_hf)
    human_loc = [s for s in alignment_hf[1] if s != '-']
    human_loc = ''.join(human_loc)
    fruit_fly_loc = [s for s in alignment_hf[2] if s != '-']
    fruit_fly_loc = ''.join(fruit_fly_loc)

    alignment_matrix_hp = student.compute_alignment_matrix(human_loc, pax,
                                                           scoring_matrix,
                                                           True)
    alignment_matrix_fp = student.compute_alignment_matrix(fruit_fly_loc, pax,
                                                           scoring_matrix,
                                                           True)
    alignment_hp = student.compute_global_alignment(human_loc, pax,
                                                    scoring_matrix,
                                                    alignment_matrix_hp)
    alignment_fp = student.compute_global_alignment(fruit_fly_loc, pax,
                                                    scoring_matrix,
                                                    alignment_matrix_fp)
    same_pre_hp = agree_precentage(alignment_hp[1], alignment_hp[2])
    same_pre_fp = agree_precentage(alignment_fp[1], alignment_fp[2])
    print 'The aggree precentage of human and pax is: %.4f%%' % same_pre_hp
    print 'The aggree precentage of fruit fly and pax is: %.4f%%' % same_pre_fp


def agree_precentage(seq_x, seq_y):
    '''
    Helper function to compute the precentage of elements in these two given
    sequences that agree
    Return a float which varies from 0 to 100(both included)
    '''
    assert len(seq_x) == len(seq_y), 'Two sequences don\'t match'
    total = len(seq_x)
    assert total != 0, 'Error, 0 will be divided'
    count_same = 0.0
    for idx in xrange(len(seq_x)):
        if seq_x[idx] == seq_y[idx]:
            count_same += 1
    return count_same / total * 100

if __name__ == '__main__':
    # question1()
    question2()