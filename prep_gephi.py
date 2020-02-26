#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx


# In[ ]:


inh = 'FPV'
vectype = 'distvec'
path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'
gephi_header = '\t'.join(['Id', 'value','class'])



# In[ ]:


def classify(val):
    return 1 if val <= 3 else 2


# In[ ]:

for splitnum in range(10):
    datafilename = 'PI_DataSet_6_19_random_split_' + str(splitnum) + '.txt'
    tree_folder = vectype + "_data/" + inh + "_random_countvec_spanning_trees/"
    treename = 'PI_DataSet_6_19_random_split_' + str(
        splitnum) + '_399nn_dist_vec_' + inh + 'filtered_spanning_tree_edges.txt'
    writefilename = 'PI_DataSet_6_19_random_split_' + str(splitnum) + '_399nn_dist_vec_' + inh + 'nodes.txt'
    writefile = path + tree_folder + writefilename
    datafile = path+datafilename
    df = open(datafile)
    header = next(df)
    inh_ind = header.index(inh)
    id_ind = 0

    f = open(writefile, 'w')
    f.write(gephi_header)
    for line in df:
        line = line.split("\t")
        id = line[id_ind]
        val = line[inh_ind]
        cl = str(classify(float(val)))
        token = '\n'+'\t'.join([id, val,cl])
        f.write(token)
    f.close()
    df.close()

