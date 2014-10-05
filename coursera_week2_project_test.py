# -*- coding: utf-8 -*-
import week2_pjt_template as wtp
import week2_pjt_cluster as wpc
from random import seed, randint

test_sample1 = [wpc.Cluster(set(), horiz_pos, 0, 1, 0)
                for horiz_pos in xrange(10)]
seed(1)
pointx = [randint(0, 10) for i in xrange(10)]
pointy = [randint(0, 10) for i in xrange(10)]
fip_code = [randint(100, 200) for i in xrange(10)]
test_sample2 = [wpc.Cluster(set([fip]), horiz_pos, vert_pos, 1, 0)
                for (fip, horiz_pos, vert_pos) in zip(fip_code, pointx, pointy)]
pointx3 = [randint(0, 100) for i in xrange(100)]
pointy3 = [randint(0, 100) for i in xrange(100)]
fip_code3 = [randint(100, 900) for i in xrange(100)]
test_sample3 = [wpc.Cluster(set([fip]), horiz_pos, vert_pos, 1, 0)
                for (fip, horiz_pos, vert_pos) in zip(fip_code3, pointx3, pointy3)]

test_sample4 = [wpc.Cluster(set([]), 0, 0, 1, 0),
                wpc.Cluster(set([]), 0, 1, 1, 0),
                wpc.Cluster(set([]), 0, 2, 1, 0)]

print "=" * 10 + "Closest pairs test" + "=" * 10
print "Sample 1"
print 'data:'
for data in test_sample1:
    print data
bfresult_sample1 = wtp.bf_closest_pairs(test_sample1)
slowresult_sample1 = wtp.slow_closest_pairs(test_sample1)
fastresult_sample1 = wtp.fast_closest_pair(test_sample1)
print "bf result", bfresult_sample1
print "slow result", slowresult_sample1
print "fast result", fastresult_sample1

print '\n'
print 'Sample 2'
print 'data:'
for data in test_sample2:
    print data
bfresult_sample2 = wtp.bf_closest_pairs(test_sample2)
slowresult_sample2 = wtp.slow_closest_pairs(test_sample2)
fastresult_sample2 = wtp.fast_closest_pair(test_sample2)
print 'bf result', bfresult_sample2
print 'slow result', slowresult_sample2
print 'fast result', fastresult_sample2

print '\n'
print 'Sample 3'
print 'data:'
for data in test_sample3:
    print data
bfresult_sample3 = wtp.bf_closest_pairs(test_sample3)
slowresult_sample3 = wtp.slow_closest_pairs(test_sample3)
fastresult_sample3 = wtp.fast_closest_pair(test_sample3)
print 'bf result', bfresult_sample3
print 'slow result', slowresult_sample3
print 'fast result', fastresult_sample3


print '\n'
print '=' * 10 + 'Clustering' + '=' * 10
print "Sample2"
print 'cluster points', zip(pointx, pointy)
hi_result_sample2 = wtp.hierarchical_clustering(test_sample2, 3)
k_reslut_sample2 = wtp.kmeans_clustering(test_sample2, 3, 10)
print 'hierachical clustering'
for result in hi_result_sample2:
    print result
print '\n'
print 'k mean clustering'
for result in k_reslut_sample2:
    print result
