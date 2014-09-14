# -*- coding: utf-8 -*-

import coursera_week1_project as cwp

# some test samples
sample1 = {1: [], 2: [], 3: [], 4: []}
sample2 = {1: [2, 3, 5],
           2: [1, 4, 6],
           3: [1, 4],
           4: [2, 3],
           5: [1],
           6: [2]}
sample3 = {1: [],
           2: [3, 4],
           3: [2],
           4: [2]}

# bfs_visited function test
sample1_bfs_visited = cwp.bfs_visited(sample1, 2)
assert sample1_bfs_visited == set([2]), 'Sample1 bfs_visited error'
sample2_bfs_visited = cwp.bfs_visited(sample2, 1)
assert sample2_bfs_visited == set(
    [1, 2, 3, 5, 4, 6]), 'Sample2 bfs_visited error'

# cc_visited function test
sample1_cc_visited = cwp.cc_visited(sample1)
assert sample1_cc_visited == [
    set([1]), set([2]), set([3]), set([4])], 'Sample1 cc_visited error'
sample2_cc_visited = cwp.cc_visited(sample2)
assert sample2_cc_visited == [
    set([1, 2, 3, 4, 5, 6])], 'Sample2 cc_visited error'

# largest_cc_size function test
sample1_largest_cc_size = cwp.largest_cc_size(sample1)
assert sample1_largest_cc_size == 1, 'Sample1 largest_cc_size error'
sample2_largest_cc_size = cwp.largest_cc_size(sample2)
assert sample2_largest_cc_size == 6, 'Sample2 largest_cc_size error'
sample3_largest_cc_size = cwp.largest_cc_size(sample3)
assert sample3_largest_cc_size == 3, 'Sample3 largest_cc_size error'

# compute_resilience function test
attack_order1 = [1, 2, 3, 4]
sample1_resilience = cwp.compute_resilience(sample1, attack_order1)
print sample1_resilience

attack_order2 = [1, 2]
sample2_resilience = cwp.compute_resilience(sample2, attack_order2)
print sample2_resilience

attack_order3 = [1, 4]
sample3_resilience = cwp.compute_resilience(sample3, attack_order3)
print sample3_resilience
