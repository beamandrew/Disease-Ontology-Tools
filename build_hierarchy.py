import DO_utils as do
from visualize_ontology import *
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

data_path = "/Users/ab455/Downloads/DOID_full_datasets/"
files = os.listdir(data_path)
data = pd.read_table(data_path+files[0])
source = files[0].split('-')[0]
data['Source'] = source
for f in files[1:len(files)]:
    file_df = pd.read_table(data_path+f)
    source = f.split('-')[0]
    file_df['Source'] = source
    data = pd.concat([data,file_df])

terms = Series(data['TERM'].values.ravel()).unique()

# Get a small section of the DO to experiment with #
base_term_id = 'DOID0050700'
base_term = 'heart disease'
base_level = levels[base_term]

## Get all of the child terms ##
child_terms = []
for term in terms:
    if term in levels:
        term_level = levels[term]
        if term != base_term:
            isap = do.is_a_parent(term,base_term,term,parents_of,parents_of[term])
            if isap and not(term in child_terms):
                child_terms.append(term)

visualize_terms(base_term,child_terms,children_of)

## Get terms count ##
term_count = {}
for term in child_terms:
    count = data[data.TERM == term].shape[0]
    term_count[term] = count
## Now find all of the valid terms ##
