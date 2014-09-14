# -*- coding: utf-8 -*-
'''
Project 2 - Connected components and graph resilience
'''

from collections import deque


def bfs_visited(ugraph, start_node):
    '''
    Takes the undirected graph ugraph and the node start_node and returns the set consisting of all nodes that are visited by a breadth-first search that starts at start_node.
    '''
    visited = list()
    visited.append(start_node)
    queue = deque()
    queue.append(start_node)

    while len(queue) > 0:
        this_node = queue.popleft()
        for neighborhood in ugraph[this_node]:
            if not (neighborhood in visited):
                visited.append(neighborhood)
                queue.append(neighborhood)
    return visited


def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets, where each set consists of all the nodes (and nothing else) in a connected component, and there is exactly one set in the list for each connected component in ugraph and nothing else.
    '''
    ans = list()
    remained = ugraph.keys()
    while len(remained) > 0:
        this_node = remained[0]
        connected_node = set(bfs_visited(ugraph, this_node))
        ans.append(connected_node)
        remained = list(set(remained).difference(connected_node))
    return ans


def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the size (an integer) of the largest connected component in ugraph.
    '''
    connected = cc_visited(ugraph)
    size_connected = [len(item) for item in connected]
    return max(size_connected)


def compute_resilience(ugraph, attack_order):
    '''
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order. For each node in the list, the function removes the given node and its edges from the graph and then computes the size of the largest connected component for the resulting graph.
    The function should return a list whose k+1th entry is the size of the largest connected component in the graph after the removal of the first k nodes in attack_order. The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    '''
    ans = []
    for attack_node in attack_order:
        largest_size = largest_cc_size(ugraph)
        ans.append(largest_size)
        ugraph = remove_node(ugraph, attack_node)
    return ans


def remove_node(ugraph, node):
    '''
    Auxiliary function to remove given node and edges from a undirected graph
    '''
    for neighborhood in ugraph[node]:
        ugraph[neighborhood] = list(set(ugraph[neighborhood]).difference(set([node])))
    ugraph.pop(node)
    return ugraph
