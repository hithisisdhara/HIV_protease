#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from collections import defaultdict
import pandas as pd
import time


########################################################################
## helper functions
#######################################################################


def read_edges(edgefile):
    f = open(edgefile)
    ans = []
    for line in f:
        line = tuple(sorted(map(lambda x: int(x), line.strip().split("\t"))))
        ans.append(line)
    return ans


def get_nodes(edges):
    nodes = set()
    for e in edges:
        nodes.update(e)
    return sorted(nodes)


def get_inhs(nodes, df):
    seqs = []
    inh_vals = []
    nodeptr = 0
    l = len(nodes)
    for line in df:
        line = line.split('\t')
        node_ind = int(line[0])  # data specific, as I know thatthte first line is ind
        if nodeptr < l and node_ind == nodes[nodeptr]:
            nodeptr += 1
            inh_vals.append(float(line[inh_ind]))
    assert l == len(inh_vals)
    df.close()
    return inh_vals


def binarize(p):
    return [node_inhclass[n] for n in p]


def last_continuous_ind(p, num):
    ptr = 0
    while ptr < len(p) and p[ptr] == num:
        ptr += 1
    return ptr - 1


def first_ind(p, num):
    return p.index(num)


def monotone_increase(p):
    return all([p[i] >= p[i - 1] for i in range(1, len(p))])


def monotone_decrease(p):
    return all([p[i] <= p[i - 1] for i in range(1, len(p))])


def percent(x, t):
    ans = x * 100.0 / t if t != 0 else 0
    return "{0:.2f}".format(ans)


def analyze(d):
    total = 0
    totals = defaultdict(int)
    saperates = []
    monotones = ["inc", "dec", "monotone"]
    for k, v in d.items():
        v = int(v)
        tokens = k.split("_")
        num, meaning = int(tokens[0]), tokens[-1]
        key = "_".join(tokens[1:])
        while len(saperates) < num + 1:
            saperates.append(defaultdict(int))
        saperates[num][key] = v
        if meaning not in monotones:
            total += v
        else:
            totals[num] += v
    assert sum(totals.values()) == total
    print(inh, " total paths analyzed:", total)
    all_keys = ["inc", "dec", "not_monotone", 'all_zeros', 'all_ones', "zero_one", "one_zero", "spikes"]
    df = pd.DataFrame(columns=all_keys + ["total"], index=range(max(totals.keys()) + 1))

    for i in range(max(totals.keys()) + 1):
        d = saperates[i]
        t = totals[i]
        vals = [percent(d[k], t) for k in all_keys] + [t]
        df.iloc[i] = vals
    print(df)


########################################################################
## global variables
#######################################################################
inh = 'SQV'
vecstring = 'count_vec'
num_nbhrs = 400
resistance_level = 3
root_threshold = 2  # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees

path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'  # where split data lies
vecname = 'distvec' if vecstring == 'dist_vec' else 'countvec'
ff = vecname + "_data/"
folder = ff + str(
    inh) + '_random_' + vecname + '_spanning_trees/'  # where spanning trees for the splits life, filtered by inhibitor != NA
spfolder = str(inh) + '_random_shortest_paths/'  # where we will be storing shortest paths
root_threshold = 2  # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees


def get_split_data_file(splitnum):
    return path + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '.txt'


def get_shortest_paths_file(splitnum):
    edgefile = get_spanning_trees_file(splitnum)
    spfile = edgefile.split(".")[0].split("/")[-1] + "_upto" + str(
        root_threshold) + "mutsroots_shortestpaths_to_leaves.txt"
    return path + folder + spfolder + spfile


def get_spanning_trees_file(splitnum):
    return path + folder + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '_' + str(
        num_nbhrs - 1) + 'nn_dist_vec_' + str(
        inh) + 'filtered_spanning_tree_edges.txt'


# stats data saved
inh_stats = defaultdict(int)
#######################################################################

for splitnum in range(10):
    t0 = time.time()
    print(str(inh), " split ", str(splitnum))
    datafile = get_split_data_file(splitnum)
    df = open(datafile)
    header = next(df).strip().split('\t')
    inh_ind = header.index(inh)

    edgefile = get_spanning_trees_file(splitnum)
    edges = read_edges(edgefile)
    nodes = get_nodes(edges)
    inh_vals = get_inhs(nodes, df)
    node_ind = {str(v): i for i, v in enumerate(nodes)}
    node_inhclass = {str(n): int(inh_vals[node_ind[str(n)]] > resistance_level) for n in nodes}

    spfile = get_shortest_paths_file(splitnum)
    f = open(spfile)

    mutation = ''
    for line in f:
        if "mutation" in line:
            if mutation:
                print('mutation:', mutation)
            mutation = str(line.strip().split(":")[1])
        else:
            line = line.strip().split(",")

            # find if the given seq is monotone in inh vals
            vals = [inh_vals[node_ind[n]] for n in line]
            '''
            inc = monotone_increase(vals)
            if inc:
                inh_stats[mutation + '_inc'] += 1
            else:
                dec = monotone_decrease(vals)
                if dec:
                    inh_stats[mutation + '_dec'] += 1
                else:
                    inh_stats[mutation + '_not_monotone'] += 1
            '''

            binary = binarize(line)
            s = sum(binary)
            if s == len(binary):
                inh_stats[mutation + '_all_ones'] += 1
            elif s == 0:
                inh_stats[mutation + '_all_zeros'] += 1
            else:
                last_cont_zero = last_continuous_ind(binary, 0)
                first_one = first_ind(binary, 1)
                last_cont_one = last_continuous_ind(binary, 1)
                first_zero = first_ind(binary, 0)
                if last_cont_zero != -1 and last_cont_zero + 1 == first_one:
                    inh_stats[mutation + '_zero_one'] += 1
                    break
                elif last_cont_one != 1 and last_cont_one + 1 == first_zero:
                    inh_stats[mutation + '_one_zero'] += 1
                else:
                    inh_stats[mutation + '_spikes'] += 1
    print('mutation,count', mutation)
    f.close()
    print(time.time() - t0)
    t0 = time.time()

analyze(inh_stats)
