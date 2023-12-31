#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#"/home/geninfo/gpola/cst/permutation_test.py" -t "/home/geninfo/gpola/cst/Phenuiviridae.tree" -m "/home/geninfo/gpola/cst/Phenuiviridae.tsv" -i1 2 -i2 1 -p 0.05 -r 10000 -o output_dir

"""permutation_test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZFGrnE6kpwFITdh3pGczIZQwm_raEaOb
"""

import pandas as pd
import numpy as np
import sys
import treeswift  # please cite https://github.com/niemasd/TreeSwift
from queue import PriorityQueue, Queue
from tqdm.notebook import trange, tqdm
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
import argparse
import os

version="1.0.2"
print('Clustering significance test {}'.format(version))

start_time = datetime.now()
call=os.path.abspath(os.getcwd())

def print_help():
  import os
  mandatory={"-t | --tree <tree_file>":"tree file in nexus format"}
  optional={"-m | --meta <tsv_file>":"metadata file in tsv format (default: 'metadata.tsv')","-i1 <integer>":"index of the column with tree lables (ex: genus names), mandatory if -m is called", "-i2 <integer>":"index of the column with lables to test (ex: access codes), mandatory if -m is called","-o | --out <string | path>":"output directory path (default='output_dir)'", "-p | --p_value <float>":"significance level for cluster selection (default=0.05)", "-r | --replicates <integer>":"number of permutation replicates (default=10000)","-v":"version","-h":"help"}
  try:
    size = int(str(os.get_terminal_size()).split("columns=")[-1].split(",")[0])
  except Exception as e:
    print(e)
    size=None
  else:
    pass
  
  if size==None:
    try:
      size = int(subprocess.check_output("tput cols", shell=True))
    except Exception as e:
      print(e)
      size=None
    else:
      pass
  
  string=''
  
  #header = ['Clustering significance test {}'.format(version)]
  header = ['(c) 2023. Bas E. Dutilh, Yasas Wijesekara & Giuliana Pola']
  header.append('For more information access: https://github.com/Yasas1994/Clustering-significance-test')
  header.append("\nUsage:")
  #header.append("permutation_test.py -conf <configuration_file>")
  header.append("permutation_test.py -t <tree_file> <optional parameters>")
  header.append("permutation_test.py -t <tree_file> -m <meta_file> -i1 <index_tree_labels> -i2 <index_test_labels> <other optional parameters>")
  header.append("\nMandatory parameters:")
  
  if size==None:
    string=''.join(header)
  else:
    for text in header:
      line=''
      while not text=='':
        i=-1
        if len(text)<=size:
          line+=text
          text=''
        else:
          part=text[0:size]
          i=part.rindex(" ")
          line+=text[0:i]  
          text=text[i+1:]
        string+=line
        string+="\n"
        line=''
  
  keys=list(mandatory.keys())
  keys.extend(list(optional.keys()))
  values=list(mandatory.values())
  values.extend(list(optional.values()))
  maxk=0
  maxv=0
  
  for key in keys:
    if len(key)>maxk:
      maxk=len(key)
  
  for key in sorted(mandatory.keys()):
    line=''
    line+='{message: <{width}} '.format(
    message=key,
    fill=' ',
    align='<',
    width=maxk,
    )
    if size==None:
      line+=mandatory[key]
      line+="\n"
      string+=line
    else:
      rest=size-maxk-1
      text=mandatory[key]
      while not text=='':
        i=-1
        if len(text)<=rest:
          if line=='':
            line+=" "*(maxk+1)
          line+=text
          text=''
        else:
          part=text[0:rest]
          i=part.rindex(" ")
          if line=='':
            line+=" "*(maxk+1)
          line+=text[0:i]  
          text=text[i+1:]
        string+=line
        string+="\n"
        line=''
  
  string += "\nOptional parameters:\n"
  
  for key in sorted(optional.keys()):
    line=''
    line+='{message: <{width}} '.format(
    message=key,
    fill=' ',
    align='<',
    width=maxk,
    )
    if size==None:
      line+=optional[key]
      line+="\n"
      string+=line
    else:
      rest=size-maxk-1
      text=optional[key]
      while not text=='':
        i=-1
        if len(text)<=rest:
          if line=='':
            line+=" "*(maxk+1)
          line+=text
          text=''
        else:
          part=text[0:rest]
          i=part.rindex(" ")
          if line=='':
            line+=" "*(maxk+1)
          line+=text[0:i]  
          text=text[i+1:]
        string+=line
        string+="\n"
        line=''

  print(string)

parser = argparse.ArgumentParser(
  prog='Clustering significance test',
  description=
  'Permutation test to test the statistical significance of clustering of different metadata annotations.',
  epilog='https://github.com/Yasas1994/Clustering-significance-test',add_help=False)

parser.add_argument('-t', '--tree', help='tree file in nexus format',)
parser.add_argument('-m', '--meta', help='metadata file in tsv format')
parser.add_argument('-i1',type=int, help='index of the column with tree lables, mandatory if -m is called')
parser.add_argument('-i2',type=int,help='index of the column with lables to test, mandatory if -m is called')
parser.add_argument('-p',
                    '--p_value',
                    help='significance level for cluster selection',type=float)
parser.add_argument('-r',
                    '--replicates',
                    help='number of permutation replicates',type=int)
parser.add_argument('-o', '--out', help='output directory path')
parser.add_argument('-h', '-help', action='store_true', help='version')
parser.add_argument('-v', action='store_true')
#parser.add_argument('-config', help='Configuration file')

args = parser.parse_args()


if not any(vars(args).values()):
    print_help()
    exit()
if "-h" in sys.argv or "--help" in sys.argv:
    print_help()
    exit()
if args.v:
    print(version)
    exit()
elif not args.tree:
    print("ERROR: Missing the tree file in nexus format (-t)!")
    exit()
elif args.meta and (not args.i1 or not args.i2):
    if not args.i1:
      print("ERROR: Missing the index of the column with tree lables (-i1)!")
    if not args.i2:
      print("ERROR: Missing the index of the column with lables to test (-i2)!")
    exit()

if not args.out:
  args.out='output_dir'
  
def rename(name):
  i=0
  path = os.path.dirname(name)
  name = os.path.basename(name)
  newname = os.path.join(path, name)
  while os.path.exists(newname):
      i += 1
      newname = os.path.join(path, "{}_{}".format(name, i))
  return newname

if args.out is not None and os.path.exists(args.out):
  args.out=rename(args.out)

os.makedirs(args.out)

try:
  log=open(os.path.join(args.out, 'file.log'), 'w')
  try:
    log.write('Clustering significance test {}\n'.format(version))
    log.write('(c) 2023. Bas E. Dutilh, Yasas Wijesekara & Giuliana Pola\n')
    log.write('For more information access: https://github.com/Yasas1994/Clustering-significance-test\n')
    log.write('\nStart time: {}\n'.format(start_time.strftime("%d/%m/%Y, %H:%M:%S")))
    log.write('\nWorking directory: {}\n'.format(call))
    log.write('\nCommand line: {}\n'.format(' '.join(sys.argv)))
    user=""
    try:
      user=os.getlogin()
    except Exception as e:
      try:
        user=os.environ['LOGNAME']
      except Exception as e:
        try:
          user=os.environ['USER']
        except Exception as e:
          pass
        else:
          pass
      else:
        pass
    else:
      pass
    if not user=="":
      log.write('\nUser: {}\n'.format(user))
    log.write('\nParameters:\n')
    for arg in vars(args):
        value = getattr(args, arg)
        if value is not None and value is not False:
            log.write("{}={}\n".format(arg,value))
    log.close()
  except Exception as e:
    print("ERROR: Log file was not written!")
    print(e)
    exit()
except Exception as e:
    print("ERROR: Log file was not created!")
    exit()

log=open(os.path.join(args.out, 'file.log'), 'a')

if not args.meta:
  message='Metadata file not provided, constructing a new metadata file.'
  args.meta='metadata.tsv'
  if (not args.i1==None) or (not args.i2==None):
    message+=' Parameters -i1 and -i2 ignored.'
  print(message)
  message+='\n'
  log.write(message)
  args.i1=2
  args.i2=1
if not args.p_value:
  args.p_value=0.05
if not args.replicates:
  args.replicates=10000

if args.meta=='metadata.tsv' and not os.path.exists(args.meta):
  args.meta = os.path.join(args.out, 'metadata.tsv')
  import re
  import random
  try:
    with open(args.tree, 'r') as file:
        tree_content = file.read()
  except Exception as e:
    print("ERROR: Tree file in nexus format (-t) was not read!")
    log.write("\nERROR: Tree file in nexus format (-t) was not read!")
    print("\nExecution time: {}".format(datetime.now() - start_time))
    log.write("\nExecution time: {}\n".format(datetime.now() - start_time))
    log.close()
    exit()
  match = re.search(r"begin trees;\n\ttree tree_1 = \[&R\] \((.*?)\);\nend;", tree_content, re.DOTALL)
  if match:
      tree_data = match.group(1)
      name_code_pairs = re.findall(r"'(.*?)_(.*?)'", tree_data)
      name_code_pairs = [(name, code) for name, code in name_code_pairs]
      random_numbers = random.sample(range(1, 99999), 10)
      table_data = []
      for name, code in name_code_pairs:
          random_number = random.choice(random_numbers)
          table_data.append([code, name, random_number])
      
      try:
        with open(os.path.join(args.out, 'metadata.tsv'), 'w') as file:
            for row in table_data:
                file.write("{}\t{}\t{}\n".format(row[0], row[1], row[2]))
      except Exception as e:
        print("ERROR: Metadata file in tsv format (-m) was not created!")
        log.write("\nERROR: Metadata file in tsv format (-m) was not created!")
        print("\nExecution time: {}".format(datetime.now() - start_time))
        log.write("\nExecution time: {}\n".format(datetime.now() - start_time))
        log.close()
        exit()
  else:
      print("ERROR: Pattern not found in tree file (-t)!")
      log.write("\nERROR: Pattern not found in tree file (-t)!")
      print("\nExecution time: {}".format(datetime.now() - start_time))
      log.write("\nExecution time: {}\n".format(datetime.now() - start_time))
      log.close()
      exit()

tree = treeswift.read_tree_nexus(args.tree)
annot = pd.read_table(args.meta, header=None)
annot[3] = annot[int(args.i1) -
                 1].astype(str) + '_' + annot[int(args.i2) - 1].astype(
                   str)  #create leaf lables

annot.columns = ['seqid', 'annot_1', 'annot_2', 'leaf_lab']

#clust = root_dist(tree['tree_1'], 4, 1 ) #get distance based clusters


# these functions were grabbed from https://github.com/niemasd/TreeCluster/blob/master/TreeCluster.py
# please cite this paper if you use this script
def root_dist(tree, threshold, support):
  leaves = prep(tree, support)
  clusters = list()
  for node in tree.traverse_preorder():
    # if I've already been handled, ignore me
    if node.DELETED:
      continue
    if node.is_root():
      node.root_dist = 0
    else:
      node.root_dist = node.parent.root_dist + node.edge_length
    if node.root_dist > threshold:
      cluster = cut(node)
      if len(cluster) != 0:
        clusters.append(cluster)
        for leaf in cluster:
          leaves.remove(leaf)

  # add all remaining leaves to a single cluster
  if len(leaves) != 0:
    clusters.append(list(leaves))
  return clusters


# initialize properties of input tree and return set containing taxa of leaves
def prep(tree, support, resolve_polytomies=True, suppress_unifurcations=True):
  if resolve_polytomies:
    tree.resolve_polytomies()
  if suppress_unifurcations:
    tree.suppress_unifurcations()
  leaves = set()
  for node in tree.traverse_postorder():
    if node.edge_length is None:
      node.edge_length = 0
    node.DELETED = False
    if node.is_leaf():
      leaves.add(str(node))
    else:
      try:
        node.confidence = float(str(node))
      except:
        node.confidence = 100.  # give edges without support values support 100
      if node.confidence < support:  # don't allow low-support edges
        node.edge_length = float('inf')
  return leaves


def cut(node):
  cluster = list()
  descendants = Queue()
  descendants.put(node)
  while not descendants.empty():
    descendant = descendants.get()
    if descendant.DELETED:
      continue
    descendant.DELETED = True
    descendant.left_dist = 0
    descendant.right_dist = 0
    descendant.edge_length = 0
    if descendant.is_leaf():
      cluster.append(str(descendant))
    else:
      for c in descendant.children:
        descendants.put(c)
  return cluster


#get all internal nodes from a tree. consider each branch as a cluster
clust_n = 0
clust_leaf = []
for branch in tree['tree_1'].traverse_postorder():
  if not branch.is_leaf():
    tmp_ = []
    for leaf in branch.traverse_leaves():
      tmp_.append([clust_n, str(leaf)])
    if len(tmp_) > 10:  #extract all branches with more than n leaves
      #print(len(tmp_))
      clust_leaf.extend(tmp_)
      clust_n += 1

clust_leaf = pd.DataFrame(clust_leaf)
clust_leaf.columns = ['cluster', 'leaf_lab']

annot = pd.merge(clust_leaf, annot, right_on='leaf_lab',
                 left_on='leaf_lab')  #add annotations to clusters

column = 'annot_2'  #only chnage this colum
#column2 = 'tmp' #simulation output is saved here

tmp = annot.groupby('cluster')[column].value_counts().sort_index()
tmp = pd.DataFrame(tmp)
tmp.columns = ['counts']
tmp.reset_index(inplace=True)
sum_cluster = tmp.groupby('cluster').sum(numeric_only=True)
max_per_cluster = tmp.groupby('cluster').max()
observed_difference_in_nps = sum(max_per_cluster['counts']) / sum(
  sum_cluster['counts']
)  #cluster purity https://stats.stackexchange.com/questions/95731/how-to-calculate-purity
observed_difference_per_cluster = np.array(max_per_cluster['counts'] /
                                           sum_cluster['counts'])

print("global cluster purity: {:.2f}".format(observed_difference_in_nps))
log.write("\nglobal cluster purity: {:.2f}".format(observed_difference_in_nps))

from tqdm import tqdm

# simulation
simulated = []
simulated_per_group = []
for _ in tqdm(range(1000)):
    annot['tmp'] = annot[column].sample(frac=1).values
    tmp2 = annot.groupby('cluster')['tmp'].value_counts().sort_index()
    tmp2 = pd.DataFrame(tmp2)
    tmp2.columns = ['counts']
    tmp2.reset_index(inplace=True)
    sum_cluster2 = tmp2.groupby('cluster').sum(numeric_only=True)
    max_per_cluster2 = tmp2.groupby('cluster').max()
    simulated_per_group.append(max_per_cluster2['counts'] / sum_cluster2['counts'])
    simulated.append(sum(max_per_cluster2['counts']) / sum(sum_cluster2['counts']))

simulated_results_per_cluster = np.array(simulated_per_group)

print("average cluster purity (permuted): {:.2f} +/- {:.2f}".format(np.mean(simulated), np.std(simulated)))
log.write("\naverage cluster purity (permuted): {:.2f} +/- {:.2f}".format(np.mean(simulated), np.std(simulated)))

"""### percluster significance (permuted)"""

significance_level = float(args.p_value)

simulations_greater_than_observed_cluster = sum(
  simulated_results_per_cluster >= observed_difference_per_cluster)
num_simulations_cluster = simulated_results_per_cluster.shape[0]
p_value = simulations_greater_than_observed_cluster / num_simulations_cluster
# Boolean which is True if significant, False otherwise
significant_or_not_cluster = p_value < significance_level

per_clust = pd.DataFrame(
  zip(np.arange(significant_or_not_cluster.shape[0]),
      significant_or_not_cluster, p_value,
      annot['cluster'].value_counts().sort_index().to_list()))
per_clust.columns = ['clusters', 'is_significant', 'p_value', 'cluster_size']

per_clust.query('is_significant == True')

annot.query('cluster == 25')
"""#### Global cluster purity (permuted)"""

simulated_results = np.array(simulated)

simulations_greater_than_observed = sum(
  simulated_results >= observed_difference_in_nps)
num_simulations = simulated_results.shape[0]
p_value = simulations_greater_than_observed / num_simulations
significant_or_not = p_value < significance_level

# Plot permutation simulations
density_plot = sns.kdeplot(simulated, fill=True, label='Permuted')
density_plot.set(xlabel='Absolute Difference cluster purity', ylabel='Proportion of Simulations', title='Permutation test for determination\n of cluster-label congruence \n{} (p = {:.2f})'.format("Test: Passed" if significant_or_not else "Test:Failed", p_value))

#report=open(os.path.join(args.out, 'report.txt'),"w")
if significant_or_not:
  log.write("\nThe analysed tree passed in the permutation test for determination of cluster-label congruence (p = {:.2f})".format(p_value))
else:
  log.write("\nThe analysed tree failed in the permutation test for determination of cluster-label congruence (p = {:.2f})".format(p_value))

# Add a line to show the actual difference observed in the data
density_plot.axvline(x=observed_difference_in_nps,
                     color='red',
                     linestyle='--',
                     label='Observed Difference')

plt.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(args.out, 'graph.png'))

print("\nExecution time: {}".format(datetime.now() - start_time))
log.write("\nExecution time: {}\n".format(datetime.now() - start_time))
print("Done.")
log.write("Done.")
log.close()
exit()