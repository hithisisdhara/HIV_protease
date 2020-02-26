#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import time
import networkx as nx
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
import os

t0 = time.time()
#######################################################################
## helper functions
#######################################################################
from utilities import *
########################################################################
## global variables
#######################################################################

inh = 'SQV'
vecstring = 'count_vec'
num_nbhrs = 400
resistance_level = 3
root_threshold = 2 # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees

path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'  # where split data lies
vecname = 'distvec' if vecstring=='dist_vec' else 'countvec'
folder = str(
	inh) + '_random_'+vecname+'_spanning_trees/'  # where spanning trees for the splits life, filtered by inhibitor != NA
spfolder = str(inh)+'_random_shortest_paths/' # where we will be storing shortest paths
root_threshold = 2 # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees

if not os.path.exists(path+folder+spfolder):
    os.makedirs(path+folder+spfolder)

#######################################################################
for splitnum in range(10):

	# data file with split data, we need the ip_val and seqs from here
	datafile = path + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '.txt'

	# edge file is the file with spanning tree edges
	writefile = path + folder + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '_'+str(num_nbhrs-1)+'nn_dist_vec_' + str(inh) + 'filtered_spanning_tree_edges.txt'

	# variables
	vectors = []
	keys = []

	f = open(datafile)
	header = next(f).split("\t")[:-1]

	inh_ind = header.index(inh)
	vec_start = header.index("dist_vec_start") if vecstring == 'dist_vec' else  header.index("count_vec_start")
	vec_end = header.index("count_vec_start") if vecstring == 'dist_vec' else  len(header)
	unique = header.index('inds')
	assert vec_start != -1  and unique != -1 and inh_ind != -1


	for line in f:
	    line = line.strip().split('\t')
	    if line[inh_ind] != 'NA':
		key = line[unique]
		keys.append(key)
		vectors.append(to_float(line[vec_start:vec_end]))
	assert len(keys)==len(vectors)
	f.close()

	print(str(inh), "split:", str(splitnum))
	print ("number of nodes:",len(keys))

	print("building ",str(num_nbhrs), "nn edges")
	nbrs = NearestNeighbors(n_neighbors=num_nbhrs, algorithm='ball_tree').fit(vectors)
	distances, indices = nbrs.kneighbors(vectors)

	pair_distance = defaultdict(float)
	for i in range(len(indices)):
	    line = indices[i]
	    for j in range(1,len(line)):
		pair = (line[0],line[j]) if line[0]<line[j] else (line[j],line[0])
		pair_distance[pair] = distances[i][j]
	print("num ",str(num_nbhrs), "nn edges:",len(pair_distance))

	del distances, indices

	edges = [list(k)+[v] for k,v in pair_distance.items()]
	del pair_distance

	print("making graph..")
	G=nx.Graph()
	G.add_weighted_edges_from(edges)
	print("making spanning tree..")
	T=nx.minimum_spanning_tree(G)

	del G, edges
	numcomps =len(list(nx.connected_components(T)))


	print ("spanning tree edges:", len(T.edges)," nodes:", len(T.nodes), "\n num comps:",numcomps)
	if numcomps != 1:
		print("WARNING: NOT A SPANNING TREE for split",str(splitnum))
		print ([len(c) for c in nx.connected_components(T)])
 

	f = open(writefile,'w')
	for e in T.edges:
		a,b = e
		token = join_as_token([keys[a],keys[b]],last=True)
		f.write(token)
	f.close()

	print ("finished split ",str(splitnum),":",time.time()-t0)
print ("finished ",inh)





