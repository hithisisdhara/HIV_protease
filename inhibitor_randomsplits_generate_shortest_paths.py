from __future__ import print_function
import networkx as nx
import time
import os
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


def get_seqs_inhs(nodes,df):
    seqs = []
    inh_vals = []
    nodeptr = 0
    l = len(nodes)
    count = 0
    for line in df:
        count += 1
        line = line.split('\t')
        node_ind = int(line[0]) # data specific, as I know thatthte first line is ind
        if nodeptr < l and node_ind == nodes[nodeptr]:
            nodeptr += 1
            seqs.append(line[seq_start:seq_end])
            inh_vals.append(float(line[inh_ind]))
    assert l == len(seqs)==len(inh_vals)
    df.close()
    return seqs,inh_vals
def is_equal(a,b):
    return all(map(lambda x:x[0]==x[1], zip(a,b)))
def count_difference(a,b):
    return sum([int(x[0]!=x[1]) for x in zip(a,b)])
letters = list("PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYDQILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF")

########################################################################
## global variables
#######################################################################
inh = 'DRV'
vecstring = 'count_vec'
num_nbhrs = 400
root_threshold = 2 # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees

path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'  # where split data lies
vecname = 'distvec' if vecstring=='dist_vec' else 'countvec'
folder = str(
	inh) + '_random_'+vecname+'_spanning_trees/'  # where spanning trees for the splits life, filtered by inhibitor != NA
spfolder = str(inh)+'_random_shortest_paths/' # where we will be storing shortest paths

if not os.path.exists(path+folder+spfolder):
    os.makedirs(path+folder+spfolder)

#######################################################################
for splitnum in range(10):

    #data file with split data, we need the ip_val and seqs from here
    datafile = path+'PI_DataSet_6_19_random_split_'+str(splitnum)+'.txt'

    # edge file is the file with spanning tree edges
    edgefile =path + folder + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '_'+str(num_nbhrs-1)+'nn_dist_vec_' + str(
		inh) + 'filtered_spanning_tree_edges.txt'

    writefile = edgefile.split(".")[0].split("/")[-1] + "_upto" + str(
        root_threshold) + "mutsroots_shortestpaths_to_leaves.txt"
    writefile = path + folder + spfolder + writefile
    df = open(datafile)
    # get necessary indices from header
    header = next(df).strip().split('\t')
    inh_ind = header.index(inh)
    seq_start = header.index('P1')
    seq_end = header.index('P99') + 1
    assert seq_start != -1 and seq_end != -1 and seq_start < seq_end


    edges = read_edges(edgefile)
    nodes = get_nodes(edges)
    node_ind = {v: i for i, v in enumerate(nodes)}

    # we won't be using the inh_vals here but making sure thatnone of it is 'NA" here
    seqs, _ = get_seqs_inhs(nodes, df) # take header off from df

    tree = nx.Graph()
    tree.add_edges_from(edges)
    assert len(tree.nodes) == len(tree.edges) + 1 # it is indeed a spanning tree

    leaves = [node for node in tree.nodes if tree.degree(node) == 1]
    mutations = list(map(lambda (x): count_difference(letters, x), seqs))

    roots_mutations = sorted([(node,mutations[node_ind[node]]) for node in tree.nodes if mutations[node_ind[node]]<=root_threshold],key=lambda x:x[1])
    print("split ", str(splitnum))
    print("num roots with leq", str(root_threshold),"mutations:",len(roots_mutations))
    print("expected paths:",len(leaves) * len(roots_mutations))


    f = open(writefile, 'w')
    print("writing to pathfile ", writefile)
    t0 = time.time()
    mut = -1
    for i in range(len(roots_mutations)):
        root, mutation = roots_mutations[i]
        if mut != mutation:
            h = "mutation:" + str(mutation) + "\n"
            f.write(h)
            mut = mutation
        shortest_paths = nx.shortest_path(tree, source=root)
        for l in leaves:
            token = ','.join([str(j) for j in shortest_paths[l]]) + "\n"
            f.write(token)
        if i % 100 == 0:
            print('writen nodes:',i, time.time() - t0)
            t0 = time.time()
    f.close()
    print("writing finished",time.time() - t0)
