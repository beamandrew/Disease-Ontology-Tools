import DO_utils as do
import pandas as pd
from pandas import Series
import os

obo_file = 'resources/HumanDO.obo'
db_file = 'resources/DOID_DB.txt'
obo = do.parse_DO_obo(obo_file)
parents_of, children_of = do.relationship_by_name(obo)

db = pd.read_table(db_file)

data_path = "data/"
files = os.listdir(data_path)
data = pd.read_table(data_path+files[0])
for f in files[1:len(files)]:
    data = pd.concat([data,pd.read_table(data_path+f)])

doids = Series(data['DOID'].values.ravel()).unique()

## Find top