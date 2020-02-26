#!/usr/bin/env python
# coding: utf-8

# In[1]:


distvecfile = 'PI_DataSet_6_19_PI_avg_dist_vec_210.txt'
expandedfile= 'PI_DataSet_6_19_expanded.txt'
countvecfile = 'PI_DataSet_6_19_PI_count_vec_210.txt'


# In[2]:


e = open(expandedfile)
d = open(distvecfile)
c = open(countvecfile)
for line in e:
    header = line.strip().split('\t')
    break


# In[3]:


def count_lines(o):
    c = 0
    for line in o:
        c += 1
    return c
'''
print [count_lines(x) for x in [e,c,d]]
'''


# In[4]:


total_lines = count_lines(d)
d = open(distvecfile)


# In[5]:


# create header for all
vec_start = header.index('P1')


# In[6]:


dvh = ['dist_vec_start']+['.' for _ in range(209)]
cvh = ['count_vec_start']+['.' for _ in range(209)]


# In[7]:


def join_as_one_line(a,b,c):
    assert len(a+b+c)==headerlength
    return '\t'.join(a+b+c)+"\n"


# In[8]:


headerlength = len(header + dvh + cvh)


# In[9]:


new_header = join_as_one_line(header , dvh , cvh)


# In[10]:


def split_fluff_and_vec(l):
    l = l.strip().split('\t')
    fluff = l[:vec_start]
    vec = l[vec_start:]
    return fluff, vec


# In[11]:


percent_split = 10
ten_p = total_lines/percent_split
path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'
writefiles = [open(path+'PI_DataSet_6_19_all_sequential_split_'+str(i)+".txt",'w') for i in range(percent_split)]
for wf in writefiles:
    wf.write(new_header)


# In[12]:


import numpy.random as random
count = -1
while count < total_lines-1:
    count += 1
    line_e = next(e)
    fluff_e, vec_e = split_fluff_and_vec(line_e)
    assert len(vec_e)==99
    line_d = next(d)
    fluff_d, vec_d = split_fluff_and_vec(line_d)
    assert fluff_e == fluff_d and len(vec_d)==210
    line_c = next(c)
    fluff_c, vec_c = split_fluff_and_vec(line_c)
    assert fluff_d == fluff_c and len(vec_c)==210
    token = join_as_one_line(fluff_e+vec_e, vec_d, vec_c)
    ind = count/ten_p
    ind = ind if ind < percent_split else ind-1
    f = writefiles[ind]
    f.write(token)
    if count % ten_p == 0:
        print count


# In[13]:


total_lines,count, len(vec_e)


# In[14]:


assert count+1 == total_lines


# In[16]:


def varify_lines(o):
    c = 0
    bad = 0
    for line in o:
        if line != '':
            try:
                assert len(line.split("\t"))==528
                c += 1
            except:
                bad += 1
                print len(line.split("\t"))
    print c, bad
    return c


# In[17]:


written_lines = 0
for i in range(10):
    new_writename = path+'PI_DataSet_6_19_all_sequential_split_'+str(i)+".txt"
    f = open(new_writename)
    num_lines = varify_lines(f) - 1
    written_lines += num_lines # remove header
    # print num_lines
    f.close()
print written_lines


# In[18]:


assert written_lines == total_lines


# In[ ]:




