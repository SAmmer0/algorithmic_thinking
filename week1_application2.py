# -*- coding: utf-8 -*-

import time
from week1_application_provided import targeted_order, delete_node, copy_graph
import matplotlib.pyplot as plt


def fast_target_order(ugraph):
    '''
    Using fast target order algorithm to generate attack order
    '''
    new_graph = copy_graph(ugraph)
    degree_set = generate_degree_set(new_graph)
    ans = []
    for k in xrange(len(new_graph) - 1, -1, -1):
        while len(degree_set[k]) > 0:
            node = degree_set[k].pop()
            for neighborhood in new_graph[node]:
                d = len(new_graph[neighborhood])
                degree_set[d] = degree_set[d].difference(set([neighborhood]))
                degree_set[d - 1].add(neighborhood)
            ans.append(node)
            delete_node(new_graph, node)
    return ans


def generate_degree_set(ugraph):
    '''
    Return a list in which a set of nodes that has k degree in position k.
    '''
    ans = [set([]) for i in xrange(len(ugraph))]
    for node in ugraph:
        ans[len(ugraph[node])].add(node)
    return ans


def plot_time(to_time, fto_time):
    '''
    Plot a graph to indicate the relationship between running time and size of undirected graph
    '''
    x_axis = [n for n in xrange(10, 1000, 10)]
    assert len(x_axis) == len(to_time), "Error to_time does not match"
    assert len(x_axis) == len(fto_time), "Error fto_time does not match"
    plt.plot(x_axis, to_time, '-b', label='Target Order Function')
    plt.plot(x_axis, fto_time, '-r', label='Fast Target Order Function')
    plt.legend(loc='upper left')
    plt.xlabel('Size of UPA Graph')
    plt.ylabel('Running Time(seconds)')
    plt.title('Running Time of Two Algorithms in Desktop Python')
    plt.show()


def main():
    '''
    Main functinon to display outcome
    '''
    from week1_application import generate_UPA
    to_time = []
    fto_time = []
    UPA_M = 5
    for n in xrange(10, 1000, 10):
        graph = generate_UPA(n, UPA_M)
        to_start_time = time.time()
        targeted_order(graph)
        to_end_time = time.time()
        this_to_time = to_end_time - to_start_time
        to_time.append(this_to_time)

        fto_start_time = time.time()
        fast_target_order(graph)
        fto_end_time = time.time()
        this_fto_time = fto_end_time - fto_start_time
        fto_time.append(this_fto_time)

    plot_time(to_time, fto_time)

if __name__ == '__main__':
    main()
