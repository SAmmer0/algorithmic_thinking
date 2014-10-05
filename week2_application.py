# -*- coding: utf-8 -*-

import random
import time
import matplotlib.pyplot as plt


def gen_random_clusters(num_clusters):
    '''
    Return a list which contains num_clusters instances of cluster
    '''
    from week2_pjt_cluster import Cluster
    ans = []
    for dummy_i in xrange(num_clusters):
        point_x = random.uniform(-1, 1)
        point_y = random.uniform(-1, 1)
        this_cluster = Cluster(set(), point_x, point_y, 1, 0)
        ans.append(this_cluster)
    return ans


def running_time(func):
    '''
    Return a function which return the running time of a given function
    '''
    def _running_time(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        using_time = end_time - start_time
        return using_time
    return _running_time


def loop_running_time(func, list_args):
    '''
    Return a list which contains the running time of the given function
    '''
    ans = []
    for input_data in list_args:
        run_func = running_time(func)
        using_time = run_func(input_data)
        ans.append(using_time)
    return ans


def plot_closest_pair(running_time_list, cluster_size):
    '''
    Plot the running time curve of two functions
    input data: running_time_list = [fast_running_time, slow_running_time]
    '''
    fast_running_time = running_time_list[0]
    slow_running_time = running_time_list[1]
    x_aix = cluster_size[:]
    plt.plot(x_aix, fast_running_time, '-r', label='Fast Closest Pair')
    plt.plot(x_aix, slow_running_time, '-g', label='Slow Closest Pair')
    plt.legend(loc='upper right')
    plt.title('Running Time of Two Closest Pair Algorithms on Desktop')
    plt.ylabel('Running Time(in seconds)')
    plt.xlabel('Size of Input Cluster')
    plt.show()


def compute_distortion(cluster_list, data_table):
    '''
    Compute distortion of a given cluster list
    '''
    distrotion = 0.0
    for cluster in cluster_list:
        distrotion += cluster.cluster_error(data_table)

    return distrotion


def main_1():
    '''
    Main function
    '''
    from week2_pjt_template import fast_closest_pair, slow_closest_pairs
    input_list = []
    for num_cluster in xrange(2, 200):
        cluster = gen_random_clusters(num_cluster)
        input_list.append(cluster)

    fast_running_time = loop_running_time(fast_closest_pair, input_list)
    slow_running_time = loop_running_time(slow_closest_pairs, input_list)
    running_time = [fast_running_time, slow_running_time]
    cluster_size = [size for size in xrange(2, 200)]
    plot_closest_pair(running_time, cluster_size)


def main_2():
    from week2_pjt_template import fast_closest_pair, slow_closest_pairs
    fast_time = []
    slow_time = []
    for num_cluster in xrange(2, 500):
        input_cluster = gen_random_clusters(num_cluster)
        fast_start_time = time.time()
        fast_closest_pair(input_cluster)
        fast_end_time = time.time()
        fast_this_time = fast_end_time - fast_start_time
        fast_time.append(fast_this_time)

        slow_start_time = time.time()
        slow_closest_pairs(input_cluster)
        slow_end_time = time.time()
        slow_this_time = slow_end_time - slow_start_time
        slow_time.append(slow_this_time)

    running_time = [fast_time, slow_time]
    cluster_size = [size for size in xrange(2, 500)]
    plot_closest_pair(running_time, cluster_size)


def test_distortation():
    from week2_pjt_cluster import Cluster
    from week2_pjt_template import hierarchical_clustering, kmeans_clustering
    fp = r'C:\Users\Howard\Desktop\agorithmic thinking\week2_data_290.csv'
    data = list()
    with open(fp, 'r') as input_data:
        for line in input_data.readlines():
            line_data = line.strip().split(',')
            line_data = [line_data[0], float(line_data[1]),
                         float(line_data[2]), int(line_data[3]),
                         float(line_data[4])]
            data.append(line_data)
    cluster_list = [Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
                    for line in data]
    heirarchical_cluster = hierarchical_clustering(cluster_list, 16)
    heirarchical_distortion = compute_distortion(heirarchical_cluster, fp)
    std_heirachical = 2.575 * 1e+11

    kmeans_cluster = kmeans_clustering(cluster_list, 16, 10)
    kmean_distortion = compute_distortion(kmeans_cluster, fp)
    std_kmean = 2.323 * 1e+11

    err = 1e+8
    print "heirachical distortion is:", heirarchical_distortion
    print "k-mean distrotion is:", kmean_distortion
    assert abs(heirarchical_distortion -
               std_heirachical) < err, 'heirachical distrotion compute error'
    assert abs(
        kmean_distortion - std_kmean) < err, 'k-mean distortion compute error'


def distortion_solver():
    from week2_pjt_cluster import Cluster
    from week2_pjt_template import hierarchical_clustering, kmeans_clustering
    fp = r'C:\Users\Howard\Desktop\agorithmic thinking\week2_data_111.csv'
    data = list()
    with open(fp, 'r') as input_data:
        for line in input_data.readlines():
            line_data = line.strip().split(',')
            line_data = [line_data[0], float(line_data[1]),
                         float(line_data[2]), int(line_data[3]),
                         float(line_data[4])]
            data.append(line_data)
    cluster_list = [Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
                    for line in data]
    heirarchical_cluster = hierarchical_clustering(cluster_list, 9)
    heirarchical_distortion = compute_distortion(heirarchical_cluster, data)

    kmeans_cluster = kmeans_clustering(cluster_list, 9, 5)
    kmean_distortion = compute_distortion(kmeans_cluster, data)

    print "heirachical distortion is: %.3e" % heirarchical_distortion
    print "k-mean distrotion is: %.3e" % kmean_distortion


def plot_cluster(num_cluster_list, distortion_list, title_msg):
    '''
    Distortion list contains two data set: [hierachical clustering result,
                                            k-mean clusting result]
    '''
    h_distortion = distortion_list[0]
    k_distortion = distortion_list[1]
    plt.plot(num_cluster_list, h_distortion, '-r',
             label='Hierachical Clustering')
    plt.plot(num_cluster_list, k_distortion, '-b',
             label='K-mean Clustering')
    plt.title(title_msg)
    plt.xlabel('Number of Output Cluster')
    plt.ylabel('Distortion')
    plt.legend(loc='upper right')
    plt.show()


def main_3():
    from week2_pjt_template import kmeans_clustering, hierarchical_clustering
    from week2_pjt_cluster import Cluster
    fp_list = [r'C:\Users\Howard\Desktop\agorithmic thinking\week2_data_111.csv',
               r'C:\Users\Howard\Desktop\agorithmic thinking\week2_data_290.csv',
               r'C:\Users\Howard\Desktop\agorithmic thinking\week2_data_896.csv'
               ]
    title_msg_list = ['Distortion of Two Different Method(111 counties)',
                      'Distortion of Two Different Method(290 counties)',
                      'Distortion of Two Different Method(896 counties)']
    for fp, title_msg in zip(fp_list, title_msg_list):
        distortion = [list(), list()]
        for num_output in xrange(6, 21):
            data = list()
            with open(fp, 'r') as input_data:
                for line in input_data.readlines():
                    line_data = line.strip().split(',')
                    line_data = [line_data[0], float(line_data[1]),
                                 float(line_data[2]), int(line_data[3]),
                                 float(line_data[4])]
                    data.append(line_data)
            cluster_list = [Cluster(set([line[0]]), line[1], line[2], line[3],
                                    line[4]) for line in data]

            h_cluster = hierarchical_clustering(cluster_list, num_output)
            h_distortion = compute_distortion(h_cluster, data)

            k_cluster = kmeans_clustering(cluster_list, num_output, 20)
            k_distortion = compute_distortion(k_cluster, data)

            distortion[0].append(h_distortion)
            distortion[1].append(k_distortion)
        output_cluster_num = [idx for idx in xrange(6, 21)]
        plot_cluster(output_cluster_num, distortion, title_msg)

if __name__ == '__main__':
    main_3()
