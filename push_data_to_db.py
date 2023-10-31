import pickle
import os
from sqlalchemy import create_engine

DB_URL = os.getenv('DB_URL')

filepath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\parsed_branded.pkl"

with open(filepath, 'rb') as f:
    parsed_df = pickle.load(f)
    
engine = create_engine(DB_URL)
parsed_df.to_sql("PARSED BRANDED FOODS", engine)
