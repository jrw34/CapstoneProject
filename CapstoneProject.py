#import required modules
import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter
from sqlalchemy import create_engine, text
import os

#import user-defined functions 
from ingredient_parser import*
from ingredient_request import*
from display_perfect_match import*
from description_query import*

#item to be searched for in DB
search_str = 'Orange Juice'.upper()

#query DB for all items containing search_str
query_df = description_query_db(search_str)

#test Orange Juice Query and Display
ingred_list_series = query_df.ingred_list
cleaned_ingreds = ingred_list_series.apply(lambda x: x.strip('{').strip('}').replace('"', ''))

print(cleaned_ingreds.iloc[:7])
print(set([i for x in cleaned_ingreds for i in x.split(',')]))


prioritize = ['Organic'.upper()]
avoid = ['Sodium Benzoate'.upper(), 'HIGH FRUCTOSE CORN SYRUP']
features = ['No Pulp'.upper()]

#assess counts from lists above for their presence in query_df  
assessed_query = assess_query(query_df, prioritize, avoid, features)

#filter assessed_query so that it only contains perfect matches
perfect_matches = perfect_match_from_assessed(assessed_query, prioritize, avoid, features)


#plot network graph of the perfect matches
display_perfect_matches(perfect_matches, search_str, prioritize, avoid, features).show()







