# -*- coding: utf-8 -*-
"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""
import math

# desktop
import week2_pjt_cluster as w2pc

# codeskulpter
# import alg_cluster as w2pc


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2

    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance
    between cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2),
            max(idx1, idx2))


def bf_closest_pairs(cluster_list):
    '''
    Brute force method to compute the closest pairs
    '''
    min_dist_pair = (float('inf'), -1, -1)
    for idx_i in xrange(len(cluster_list) - 1):
        for idx_j in xrange(idx_i + 1, len(cluster_list)):
            min_dist_pair = min(
                min_dist_pair, pair_distance(cluster_list, idx_i, idx_j))
    return min_dist_pair


def slow_helper(cluster_list):
    '''
    Helper function which will implement most work for the slow_closest_pairs
    '''
    pass


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm

    Returns the set of all tuples of the form (dist, idx1, idx2)
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance
    dist.

    """
    # base case
    if len(cluster_list) <= 3:
        return bf_closest_pairs(cluster_list)

    # divided and conque
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx)
                        for idx in xrange(len(cluster_list))]
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1]
                   for idx in xrange(len(hcoord_and_index))]

    m_idx = len(horiz_order) / 2
    horiz_left_order = horiz_order[:m_idx]
    horiz_right_order = horiz_order[m_idx:]
    horiz_mid = (cluster_list[horiz_order[m_idx - 1]].horiz_center() +
                 cluster_list[horiz_order[m_idx]].horiz_center()) / 2.0
    horiz_left = [cluster_list[idx] for idx in horiz_left_order]
    horiz_right = [cluster_list[idx] for idx in horiz_right_order]

    left_pairs = slow_closest_pairs(horiz_left)
    left_pairs = (left_pairs[0], horiz_left_order[left_pairs[1]],
                  horiz_left_order[left_pairs[2]])

    right_pairs = slow_closest_pairs(horiz_right)
    right_pairs = (right_pairs[0], horiz_right_order[right_pairs[1]],
                   horiz_right_order[right_pairs[2]])

    min_dist_pair = min(left_pairs, right_pairs)

    # merge
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx)
                        for idx in xrange(len(cluster_list))
                        if (abs(cluster_list[idx].horiz_center() - horiz_mid)
                            < min_dist_pair[0])]
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1]
                  for idx in xrange(len(vcoord_and_index))]

    for idx_i in xrange(len(vert_order) - 1):
        for idx_j in xrange(idx_i + 1, min(len(vert_order), idx_i + 4)):
            min_dist_pair = min(min_dist_pair,
                                pair_distance(cluster_list, idx_i, idx_j))
    return min_dist_pair


def in_interval(centre, dist):
    '''
    Return a function which is used to judge whether a point is in the given
    area
    '''
    def _in_interval(horiz_and_idx):
        if abs(centre - horiz_and_idx[0]) <= dist:
            return True
        else:
            return False
    return _in_interval


def fast_helper(cluster_list, horiz_order, vert_order):
    """
    Divide and conquer method for computing distance between closest pair of
    points
    Running time is O(n * log(n))

    horiz_order and vert_order are lists of indices for clusters
    ordered horizontally and vertically

    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """

    # base case
    if len(horiz_order) <= 3:
        bf_cluster_list = [cluster_list[idx] for idx in horiz_order]
        bf_result = bf_closest_pairs(bf_cluster_list)
        ans = (bf_result[0],
               min(horiz_order[bf_result[1]], horiz_order[bf_result[2]]),
               max(horiz_order[bf_result[1]], horiz_order[bf_result[2]]))
        return ans

    # divide
    m_idx = len(horiz_order) / 2
    horiz_mid = (cluster_list[horiz_order[m_idx - 1]].horiz_center()
                 + cluster_list[horiz_order[m_idx]].horiz_center()) / 2.0

    left_horiz_order = horiz_order[:m_idx]
    right_horiz_order = horiz_order[m_idx:]

    left_horiz_set = set(left_horiz_order)
    left_vert_order = [idx for idx in vert_order
                       if idx in left_horiz_set]

    right_horiz_set = set(right_horiz_order)
    right_vert_order = [idx for idx in vert_order
                        if idx in right_horiz_set]

    left_pairs = fast_helper(cluster_list, left_horiz_order, left_vert_order)
    right_pairs = fast_helper(cluster_list,
                              right_horiz_order, right_vert_order)
    min_dist_pair = min(left_pairs, right_pairs)
    min_dist = min_dist_pair[0]

    # conquer
    # horiz_and_idx = [(cluster_list[idx].horiz_center(), idx)
    #                  for idx in vert_order]
    # judge_in_interval = in_interval(horiz_mid, min_dist)
    # filte_res = filter(judge_in_interval, horiz_and_idx)
    # cross_vert_order = [item[1] for item in filte_res]
    cross_vert_order = [idx for idx in vert_order
                        if (abs(cluster_list[idx].horiz_center() - horiz_mid) <
                            min_dist)]
    for idx_i in xrange(len(cross_vert_order) - 1):
        for idx_j in xrange(idx_i + 1, min(len(cross_vert_order), idx_i + 4)):
            min_dist_pair = min(min_dist_pair,
                                pair_distance(cluster_list,
                                              cross_vert_order[idx_i],
                                              cross_vert_order[idx_j]))

    return min_dist_pair


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm

    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """

    # compute list of indices for the clusters ordered in the horizontal
    # direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx)
                        for idx in range(len(cluster_list))]
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1]
                   for idx in range(len(hcoord_and_index))]

    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx)
                        for idx in range(len(cluster_list))]
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1]
                  for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return answer


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list

    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    ans = [cluster.copy() for cluster in cluster_list]
    while len(ans) > num_clusters:
        closest = fast_closest_pair(ans)
        ans[closest[1]].merge_clusters(ans[closest[2]])
        ans.remove(ans[closest[2]])
    return ans


def find_closest(cluster, centers):
    '''
    Find the index of the cluster which is closest to the given cluster
    '''
    ans = [(math.sqrt((cluster.horiz_center() - point[0]) ** 2 +
                      (cluster.vert_center() - point[1]) ** 2), idx)
           for idx, point in enumerate(centers)]
    closest = min(ans)
    return closest[1]


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters

    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # initialize k-means clusters to be initial clusters with largest
    # populations
    population = [(cluster.total_population(),
                   (cluster.horiz_center(), cluster.vert_center()))
                  for cluster in cluster_list]
    population.sort(reverse=True)
    centers = [point[1] for point in population[:num_clusters]]
    for dummy_i in xrange(num_iterations):
        ans = [w2pc.Cluster(set(), 0, 0, 0, 0)
               for dummy_i in xrange(num_clusters)]
        for idx in xrange(len(cluster_list)):
            closest_idx = find_closest(cluster_list[idx], centers)
            ans[closest_idx].merge_clusters(cluster_list[idx])
        centers = [(cluster.horiz_center(), cluster.vert_center())
                   for cluster in ans]
    return ans
