import DO_utils as do
import pandas as pd
from pandas import Series
import os

obo_file = 'resources/HumanDO.obo'
db_file = 'resources/DOID_DB.txt'
obo = do.parse_DO_obo(obo_file)
parents_of, children_of = do.relationship_by_name(obo)
levels = {}
## This call modifies levels in-place ##
do.get_level(obo,'disease',children_of,0,levels)

db = pd.read_table(db_file)

data_path = "data/"
files = os.listdir(data_path)
data = pd.read_table(data_path+files[0])
for f in files[1:len(files)]:
    data = pd.concat([data,pd.read_table(data_path+f)])

terms = Series(data['TERM'].values.ravel()).unique()

hier = {}
## Find top ##
for term in terms:
    term_level = levels[term]
    for parent in terms:
        parent_level = levels[parent]
        if term != parent:
            isap = do.is_a_parent(term,parent,parent_level,term,term_level,parents_of)
            if isap:
                if term in hier:
                    hier[term].append([parent,parent_level])
                else:
                    hier[term] = [parent,parent_level]