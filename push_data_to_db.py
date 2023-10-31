import pickle
import os
from sqlalchemy import create_engine

#extract DB_URL
DB_URL = os.environ['DB_URL']
#create engine to connect to postgres DB
engine = create_engine(DB_URL)

#create filepath to load pkl file 
filepath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\parsed_branded.pkl"

with open(filepath, 'rb') as f:
    parsed_df = pickle.load(f)
    
#create new table in DB consisting of parsed branded food items dataset
parsed_df.to_sql("PARSED BRANDED FOODS", engine)
