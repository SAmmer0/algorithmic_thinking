# -*- coding: utf-8 -*-

import coursera_week0_application as cw0a
import UPA as upa
import coursera_week1_project as cw1p
from random import shuffle
import matplotlib.pyplot as plt


def generate_UPA(num_n, num_m):
    '''
    Using UPA algorithm to generate UPA graph
    '''
    ans = cw0a.generate_complete_graph(num_m)
    choosing_tril = upa.UPATrial(num_m)
    for node in xrange(num_m, num_n):
        choose_nodes = choosing_tril.run_trial(num_m)
        ans[node] = list(choose_nodes)
        for ch_node in choose_nodes:
            ans[ch_node].append(node)
    return ans


def random_order(graph):
    '''
    Generate random order of the node from given graph
    '''
    node_list = graph.keys()
    shuffle(node_list)
    return node_list


def plot_curves(*args):
    '''
    Using data plot curves, to compare the differences between these graphs
    '''
    color_styles = ['-b', '-g', '-r', '-c', '-m', '-y', '-k', '-w']
    if len(args) > len(color_styles):
        print 'Error, Too many arguments!'
        return
    for idx, curve in enumerate(args):
        x_axis = [x for x in xrange(curve[1] + 1)]
        y_axis = curve[0]
        plt.plot(x_axis, y_axis, color_styles[idx], label=curve[2])
    plt.legend(loc='upper right')
    plt.text(1000, 500, 'p=%.4f' % (3112.0 / (1346.0 * 1347 / 2)))
    plt.text(1000, 400, 'n=1347, m=2')
    plt.xlabel('Number of node removal')
    plt.ylabel('Resilience')
    plt.title('Resilience of Computer Network')
    plt.show()


def main():
    '''
    Main running function
    '''
    ER_P = 3112.0 / (1346.0 * 1347 / 2)
    UPA_M = int(3112.0 / 1347)
    UPA_N = 1347
    example_graph = cw0a.data2graph(
        r'C:\Users\Howard\Desktop\agorithmic thinking\data_week1.txt', 1347, 3112, True)
    ER_graph = cw0a.generate_ER(1347, ER_P, False)
    UPA_graph = generate_UPA(UPA_N, UPA_M)
    example_atk_order = random_order(example_graph)
    assert len(example_atk_order) == len(example_graph.keys()
                                         ), 'Error, example graph does match its random order'
    ER_atk_order = random_order(ER_graph)
    assert len(ER_atk_order) == len(ER_graph.keys()
                                    ), 'Error, ER graph does not match its random order'
    UPA_atk_order = random_order(UPA_graph)
    assert len(UPA_atk_order) == len(UPA_graph.keys()
                                     ), 'Error, UPA graph does match its random order'
    example_resilience = cw1p.compute_resilience(
        example_graph, example_atk_order)
    assert len(example_resilience) == len(
        example_atk_order) + 1, 'Error, example graph resilience does not match'
    ER_resilience = cw1p.compute_resilience(ER_graph, ER_atk_order)
    assert len(ER_resilience) == len(
        ER_atk_order) + 1, 'Error, ER graph resilience does not match'
    UPA_resilience = cw1p.compute_resilience(UPA_graph, UPA_atk_order)
    assert len(UPA_resilience) == len(
        UPA_atk_order) + 1, 'Error, UPA graph resilience does not match'
    example_plot_msg = (example_resilience, len(
        example_atk_order), 'Given Computer Network', None)
    ER_plot_msg = (
        ER_resilience, len(ER_atk_order), 'ER Graph')
    UPA_plot_msg = (UPA_resilience, len(
        UPA_atk_order), 'UPA Graph', 'n = 1347, m = 3112')
    plot_curves(example_plot_msg, ER_plot_msg, UPA_plot_msg)


if __name__ == '__main__':
    main()
