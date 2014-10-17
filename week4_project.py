# -*- coding: utf-8 -*-
'''
Computing alignments of sequences
'''


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Return a dictionary of dictionaries whose entries are indexed by pairs of
    characters in alphabet plus '-'. The score for any entry indexed by one or
    more dashes is dash_score. The score for the remaining diagonal entries is
    diag_score. Finally, the score for the remaining off-diagonal entries is
    off_diag_score.
    '''
    alphabet = list(alphabet)
    ans = dict()
    for row_item in alphabet:
        ans[row_item] = dict()
        for col_item in alphabet:
            if (row_item == '-') or (col_item == '-'):
                ans[row_item][col_item] = dash_score
            elif row_item == col_item:
                ans[row_item][col_item] = diag_score
            else:
                ans[row_item][col_item] = off_diag_score
    return ans


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix. The function computes and
    returns the alignment matrix for seq_x and seq_y
    If global_flag is True, the function will compute a global alignment
    '''
    len_x = len(seq_x)
    len_y = len(seq_y)
    ans = [[0 for dummy_j in xrange(len_y + 1)]
           for dummy_i in xrange(len_x + 1)]

    ans[0][0] = 0

    for idx in xrange(1, len_x + 1):
        ans[idx][0] = ans[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]['-']
        if not global_flag:
            ans[idx][0] = max(0, ans[idx][0])

    for idx in xrange(1, len_y + 1):
        ans[0][idx] = ans[0][idx - 1] + scoring_matrix[seq_y[idx - 1]]['-']
        if not global_flag:
            ans[0][idx] = max(0, ans[0][idx])

    for idx_i in xrange(1, len_x + 1):
        for idx_j in xrange(1, len_y + 1):
            ans[idx_i][idx_j] = max(ans[idx_i - 1][idx_j] +
                                    scoring_matrix[seq_x[idx_i - 1]]['-'],
                                    ans[idx_i][idx_j - 1] +
                                    scoring_matrix[seq_y[idx_j - 1]]['-'],
                                    ans[idx_i - 1][idx_j - 1] +
                                    scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]])
            if not global_flag:
                ans[idx_i][idx_j] = max(0, ans[idx_i][idx_j])
    return ans


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix. This function computes a 
    global alignment of seq_x and seq_y using the global alignment matrix 
    alignment_matrix.
    '''
    idx_x = len(seq_x)
    idx_y = len(seq_y)
    x_align = ''
    y_align = ''

    while (idx_x != 0) and (idx_y != 0):
        if (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] +\
            scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]):
            x_align = seq_x[idx_x - 1] + x_align
            y_align = seq_y[idx_y - 1] + y_align
            idx_x -= 1
            idx_y -= 1
        elif (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] +\
              scoring_matrix[seq_x[idx_x - 1]]['-']):
            x_align = seq_x[idx_x - 1] + x_align
            y_align = '-' + y_align
            idx_x -= 1
        else:
            x_align = '-' + x_align
            y_align = seq_y[idx_y - 1] + y_align
            idx_y -= 1

    while idx_x != 0:
        x_align = seq_x[idx_x - 1] + x_align
        y_align = '-' + y_align
        idx_x -= 1
    while idx_y != 0:
        x_align = '-' + x_align
        y_align = seq_y[idx_y - 1] + y_align
        idx_y -= 1

    alignment_score = compute_alignment_score(x_align, y_align, scoring_matrix)
    return (alignment_score, x_align, y_align)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common 
    alphabet with the scoring matrix scoring_matrix. This function computes a 
    local alignment of seq_x and seq_y using the local alignment matrix 
    alignment_matrix.
    '''
    idx_x, idx_y = find_max(alignment_matrix)
    x_align = ''
    y_align = ''

    while alignment_matrix[idx_x][idx_y] != 0:
        if (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] +\
            scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]):
            x_align = seq_x[idx_x - 1] + x_align
            y_align = seq_y[idx_y - 1] + y_align
            idx_x -= 1
            idx_y -= 1
        elif (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] +\
              scoring_matrix[seq_x[idx_x - 1]]['-']):
            x_align = seq_x[idx_x - 1] + x_align
            y_align = '-' + y_align
            idx_x -= 1
        else:
            x_align = '-' + x_align
            y_align = seq_y[idx_y - 1] + y_align
            idx_y -= 1
        
    alignment_score = compute_alignment_score(x_align, y_align, scoring_matrix)
    return (alignment_score, x_align, y_align)


def find_max(alignment_matrix):
    '''
    Helper function to find the indices of the maximum score
    '''
    max_val = float('-inf')
    idx_max = (-1, -1)
    row_len = len(alignment_matrix)
    col_len = len(alignment_matrix[0])

    for idx_row in xrange(row_len):
        for idx_col in xrange(col_len):
            if alignment_matrix[idx_row][idx_col] > max_val:
                max_val = alignment_matrix[idx_row][idx_col]
                idx_max = (idx_row, idx_col)
    return idx_max


def compute_alignment_score(seq_x, seq_y, scoring_matrix):
    '''
    Heler function which is used to compute score for given alignment
    '''
    assert len(seq_x) == len(seq_y), "Error, two sequences don\'t match"
    score = 0
    for idx in xrange(len(seq_x)):
        score += scoring_matrix[seq_x[idx]][seq_y[idx]]
    return score


def compute_alignment(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Combine compute alignment_matrix and compute_global/local_alignment
    return required alignment only
    """
    alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix,
                                                global_flag)
    if global_flag:
        alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix,
                                             alignment_matrix)
    else:
        alignment = compute_local_alignment(seq_x, seq_y, scoring_matrix,
                                            alignment_matrix)
    return alignment