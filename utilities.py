import os 
import numpy as np
import matplotlib.pyplot as plt 

##############################################
# Read and write functionalities 
def process_line(l,delemiter="\t"):
    return l.strip().split(delemiter)



def calculate_class(val, threshold = 3.0):
        try:
            val = float(val)
            decision = 1 if val <= threshold else 2
        except: 
            decision = -1
        yield str(decision)


def write_line(line, openfile,delemiter=","):
    if isinstance(line,(list,)):
        line = delemiter.join([str(x) for x in line])
    openfile.write(line+"\n")
    
def make_write_path(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
        
def read_vector(l,start,end):
    return [float(x) for x in l[start:end]]

def printfour(d):
    return str(round(d,4))

num_nbhrs = 400
resistance_level = 3
root_threshold = 2  # Threshold for which nodes wihh <= this number of mutations are selected for spanning trees

path = '/home/dshah8/Documents/Summer19/Harrison/data_ten_chunks/'  # where split data lies
def get_vecname(vecstring):
    return'distvec' if vecstring == 'dist_vec' else 'countvec'


def get_spanning_trees_folder(inh, vec_string):
    vecname = get_vecname(vec_string)
    ff = vecname + "_data/"
    folder = ff + str(inh) + '_random_' + vecname + '_spanning_trees/' 
    return folder 

def get_shortest_path_folder(inh,vec_string): 
    folder = get_spanning_trees_folder(inh, vec_string)
    spfolder = str(inh) + '_random_shortest_paths/'  # where we will be storing shortest paths
    return path+folder + spfolder


def get_split_data_file(splitnum):
    return path + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '.txt'

def get_shortest_paths_file(splitnum, inh, vec_string, root_threshold=2):
    edgefile = get_spanning_trees_file(splitnum,inh, vec_string)
    spfile = edgefile.split(".")[0].split("/")[-1] + "_upto" + str(
        root_threshold) + "mutsroots_shortestpaths_to_leaves.txt"
    return  get_shortest_path_folder(inh,vec_string) + spfile


def get_spanning_trees_file(splitnum,inh, vec_string):
    folder = get_spanning_trees_folder(inh, vec_string)
    return path + folder + 'PI_DataSet_6_19_random_split_' + str(splitnum) + '_' + str(
        num_nbhrs - 1) + 'nn_dist_vec_' + str(
        inh) + 'filtered_spanning_tree_edges.txt'

def get_sparkfilename(inh,vec_string):
    return get_shortest_path_folder(inh,vec_string)+"pysparkdata.csv"

def separate(l):
    a,b = [],[]
    for t in l:
        a.append(t[0])
        b.append(t[1])
    return a,b 

figfilepath = '/home/dshah8/Documents/Summer19/Harrison/'
def get_figfile(inh,vectype,pathtype):
    vecname = get_vecname(vectype)
    folder = figfilepath+vecname+"_figs/"
    make_write_path(folder)
    plottype = None 
    if pathtype in ["gains", "looses", "spikes"]:
        plottype = "resistance_length_vs_variance_scatterplot.png"
    elif pathtype == "above":
        plottype = "variance_histogram.png"
    else:
        print("error in pathtype")
        return
    filename = folder+inh+"_"+vecname+"_"+pathtype+"_"+plottype
    return filename


####################################
# Drawing 
####################################
def draw_bar(yvals,xtickvals):
    ypos = range(len(yvals))
    plt.bar(ypos,yvals)
    plt.xticks(ypos,xtickvals[-len(ypos):],rotation = 45)
    
def draw_scatter(x,y,ptsize):
    plt.scatter(x,y,s=ptsize, color = 'k')
    
def draw_plot(x):
    plt.plot(x)