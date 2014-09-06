# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from cmath import log
from random import random
import DPA as dpa


def data2graph(fp=r'C:\users\howard\desktop\data1.txt'):
    '''
    Convert data in txt file to dictionary formated graph
    '''
    data_file = open(fp, 'r')
    data = {}
    for line in data_file.readlines():
        d = line.strip().split()
        data[int(d[0])] = [int(s) for s in d[1:]]
    return data


def compute_in_degree(digraph):
    '''
    Compute in-degree for a direct graph, return a dictionary to
    represent in-degree for every node
    '''
    ans = {}
    for node in digraph.keys():
        if not ans.has_key(node):
            ans[node] = 0
        for di_node in digraph[node]:
            if not ans.has_key(di_node):
                ans[di_node] = 1
            else:
                ans[di_node] += 1
    return ans


def in_degree_distribution(digraph):
    '''
    Compute in-degree distribution for a direct graph
    '''
    in_degree = compute_in_degree(digraph)
    ans = {}
    for node, degree in in_degree.items():
        if not ans.has_key(degree):
            ans[degree] = 1
        else:
            ans[degree] += 1
    return ans


def normalize_distribution(distribution):
    '''
    Normalize a in-degree distribution, that is, make value in
    distribution dictionary sum to 1
    '''
    ans = {}
    in_degree_sum = 0
    for key, value in distribution.items():
        in_degree_sum += value
    for key, value in distribution.items():
        ans[key] = float(value) / in_degree_sum
    return ans


def plot_log(nor_distribution):
    '''
    Using normalized distribution to plot log/log graph
    '''
    degree_list = sorted(nor_distribution.keys())[1:]
    value_list = []
    for degree in degree_list:
        value_list.append(nor_distribution[degree])
    degree_x = [log(item) for item in degree_list]
    value_y = [log(item) for item in value_list]
    plt.plot(degree_x, value_y, 'ro')
    plt.ylabel('log(distribution)')
    plt.xlabel('log(degree)')
    plt.show()


def generate_ER(node_num, p):
    '''
    Generate a random graph
    '''
    ans = {}
    for node_i in xrange(node_num):
        ans[node_i] = []
        for node_j in xrange(node_num):
            if node_i == node_j:
                continue
            rnd = random()
            if rnd < p:
                ans[node_i].append(node_j)
    return ans


def generate_complete_graph(n):
    '''
    Return a complete direct graph
    '''
    ans = {}
    for node in xrange(n):
        ans[node] = [item for item in xrange(n) if item != node]
    return ans


def generate_DPA(num_n, num_m):
    '''
    Using DPA algorithm to generate a random graph
    '''
    ans = generate_complete_graph(num_m)
    choosing_tril = dpa.DPATrial(num_m)
    for node in xrange(num_m, num_n):
        choosing_nodes = choosing_tril.run_trial(num_m)
        ans[node] = list(choosing_nodes)
    return ans


def main1():
    data = data2graph()
    in_degree = in_degree_distribution(data)
    nor_distribution = normalize_distribution(in_degree)
    plot_log(nor_distribution)


def main_rand():
    node_num = 10000
    probability = 0.001
    rand_graph = generate_ER(node_num, probility)
    in_degree = in_degree_distribution(rand_graph)
    nor_distribution = normalize_distribution(in_degree)
    plot_log(nor_distribution)


def main_DPA():
    num_n = 27770
    num_m = 13
    DPA_graph = generate_DPA(num_n, num_m)
    in_degree = in_degree_distribution(DPA_graph)
    nor_distribution = normalize_distribution(in_degree)
    plot_log(nor_distribution)

if __name__ == '__main__':
    main_DPA()
