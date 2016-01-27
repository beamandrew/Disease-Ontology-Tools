import DO_utils
import pandas as pd
from pandas import Series
import os

obo_file = 'resources/HumanDO.obo'
obo = DO_utils.parse_DO_obo(obo_file)

data_path = "data/"
files = os.listdir(data_path)
data = pd.read_table(data_path+files[0])
for f in files[1:len(files)]:
    data = pd.concat([data,pd.read_table(data_path+f)])

doids = Series(data['DOID'].values.ravel()).unique()
