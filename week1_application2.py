# -*- coding: utf-8 -*-

import time
import week1_application as w1a
from week1_application_provided import targeted_order, delete_node


def fast_target_order(ugraph):
    '''
    Using fast target order algorithm to generate attack order
    '''
    degree_set = generate_degree_set(ugraph)
    ans = []
    for k in xrange(len(ugraph) - 1, 0, -1):
        while len(degree_set[k]) > 0:
            node = degreee_set[k].pop()
            for neighborhood in ugraph[node]:
                d = len(ugrph[neighborhood])
                degree_set[d] = degree_set[d].difference(set([neighborhood]))
                degree_set[d - 1].add(neighborhood)
            ans.append(node)
            delete_node(ugraph, node)
    return ans



def generate_degree_set(ugraph):
    '''
    Return a list in which a set of nodes that has k degree in position k.
    '''
    ans = [set([]) for i in xrange(len(ugraph))]
    for node in ugraph:
        ans[len(ugrph[node])].add(node)
    return ans
