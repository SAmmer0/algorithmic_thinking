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


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Generate distribution of score using random method
    """
    ans = dict()
    for trial in xrange(num_trials):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = ''.join(rand_y)
        alignment = student.compute_alignment(seq_x, rand_y, scoring_matrix,
                                              False)
        score = alignment[0]
        ans.setdefault(score, 0)
        ans[score] += 1
    return ans


def score_normalization(score):
    """
    Return a normalized score distribution, tuple of two list, one for score,
    one for frenquence
    """
    score_copy = dict()
    for key in score:
        score_copy[key] = score[key]

    total = 0.0

    for key in score_copy:
        total += score_copy[key]

    for key in score_copy:
        score_copy[key] /= total

    score_list = sorted(score_copy.keys())
    frenquency_list = [score_copy[key] for key in score_list]

    return score_list, frenquency_list


def plot_distribution(x_axis, y_axis):
    """
    Plot bar graph for given distribution
    """
    plt.bar(x_axis, y_axis, color='b')
    plt.xlabel("Score")
    plt.ylabel("Frenquence")
    plt.title("Distribution of Score")
    plt.show()


def mean(distribution):
    """
    Compute the mean value of a given distribution
    The distribution is normalized and given as a tuple, formated as
    (value_list, frenquence_list)
    """
    ans = 0.0
    for value, frenquency in zip(distribution[0], distribution[1]):
        ans += value * frenquency
    return ans


def std_deviation(distribution):
    """
    Compute the standard deviation of a given distribution
    The distribution is given as a dictionary(normalized)
    """
    total = 0.0
    mu = mean(distribution)
    for value, frenquency in zip(distribution[0], distribution[1]):
        total += ((value - mu) ** 2) * frenquency
    total = math.sqrt(total)
    return total


def z_score(score, mean, sd):
    """
    Compute z-score
    """
    return float((score - mean) / sd)


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


def generate_random_seq(seq_len, choosing_list):
    '''
    Generate a random sequence which has a length of seq_len, elements are
    choosing from choosing_list
    '''
    ans = list()
    choosing_list = list(choosing_list)
    for idx in xrange(seq_len):
        this_element = random.choice(choosing_list)
        ans.append(this_element)
    return ''.join(ans)


def question3():
    '''
    Solution for question 3
    '''
    amino_acids = 'ACBEDGFIHKMLNQPSRTWVYXZ'
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    human = read_protein(HUMAN_EYELESS_URL)
    fruit_fly = read_protein(FRUITFLY_EYELESS_URL)

    random_human = generate_random_seq(len(human), amino_acids)
    random_fruitfly = generate_random_seq(len(fruit_fly), amino_acids)

    # question 1
    alignment_matrix_loc = student.compute_alignment_matrix(random_human,
                                                            random_fruitfly,
                                                            scoring_matrix,
                                                            False)
    alignment_loc = student.compute_local_alignment(random_human,
                                                    random_fruitfly,
                                                    scoring_matrix,
                                                    alignment_matrix_loc)
    print "Local alignment:"
    print "Score:", alignment_loc[0]
    print "Random human:", alignment_loc[1]
    print "Random fruit fly:", alignment_loc[2]

    # question 2
    pax = read_protein(CONSENSUS_PAX_URL)
    random_human_loc = [s for s in alignment_loc[1] if s != '-']
    random_human_loc = ''.join(random_human_loc)

    random_fruitfly_loc = [s for s in alignment_loc[2] if s != '-']
    random_fruitfly_loc = ''.join(random_fruitfly_loc)

    alignment_matrix_hp = student.compute_alignment_matrix(random_human_loc,
                                                           pax,
                                                           scoring_matrix,
                                                           True)
    alignment_matrix_fp = student.compute_alignment_matrix(random_fruitfly_loc,
                                                           pax,
                                                           scoring_matrix,
                                                           True)

    alignment_hp = student.compute_global_alignment(random_human_loc, pax,
                                                    scoring_matrix,
                                                    alignment_matrix_hp)
    alignment_fp = student.compute_global_alignment(random_fruitfly_loc, pax,
                                                    scoring_matrix,
                                                    alignment_matrix_fp)

    same_pre_hp = agree_precentage(alignment_hp[1], alignment_hp[2])
    same_pre_fp = agree_precentage(alignment_fp[1], alignment_fp[2])
    print "The aggree precentage of random human and pax is: %.3f%%" % same_pre_hp
    print "The aggree precentage of random fruitfly and pax is: %.3f%%" % same_pre_fp


def question45():
    """
    Solution for question 4 and 5
    """
    human = read_protein(HUMAN_EYELESS_URL)
    fruitfly = read_protein(FRUITFLY_EYELESS_URL)
    scoring_matrix = read_scoring_matrix(PAM50_URL)

    alignment_hf = student.compute_alignment(human, fruitfly, scoring_matrix,
                                             False)

    random.seed(1000)
    alignment_score = generate_null_distribution(human, fruitfly,
                                                 scoring_matrix, 1000)
    score, frenquency = score_normalization(alignment_score)
    
    with open('backup.csv', 'w', ) as backup:
        for s, f in zip(score, frenquency):
            backup.write(str(s) + ',' + str(f) + '\n')

    mu = mean((score, frenquency))
    sd = std_deviation((score, frenquency))
    zscore = z_score(alignment_hf[0], mu, sd)

    print "Mean of generated distribution is:", mu
    print "standard deviation of generated distribution is:", sd
    print "z-score for human vs. fruitfly is:", zscore

    plot_distribution(score, frenquency)


if __name__ == '__main__':
    # question1()
    # question2()
    # question3()
    question45()
