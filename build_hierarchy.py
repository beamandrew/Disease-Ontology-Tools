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

data_path = "/Users/ab455/Downloads/DOID_full_datasets/"
files = os.listdir(data_path)
data = pd.read_table(data_path+files[0])
for f in files[1:len(files)]:
    data = pd.concat([data,pd.read_table(data_path+f)])

terms = Series(data['TERM'].values.ravel()).unique()

# Get a small section of the DO to experiment with #
base_term_id = 'DOID1287'
base_term = 'cardiovascular system disease'
base_level = level[base_term]

## Get all of the child terms ##
child_terms = []
## Find top ##
for term in terms:
    if term in levels:
        term_level = levels[term]
        if term != parent:
            isap = do.is_a_parent(term,base_term,0,term,term_level,parents_of)
            if isap and not(term in child_terms):
                child_terms.append(term)


## Get all of the pages with one of these terms ##
term_data = data[data['TERM'].isin(child_terms)]

## Now we're going to make an article x term matrix to keep to store everything ##
out_data = pd.DataFrame(columns = child_terms)
