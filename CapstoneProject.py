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
from ingredient_query import*
from display_perfect_match import*
from description_query import*

#item to be searched for in DB
search_str = 'Orange Juice'.upper()

#query DB for all items containing search_str
query_df = ingredient_query(search_str)

#test Orange Juice Query and Display

prioritize = ['Organic']
avoid = ['Sugar', 'Sodium Benzoate', 'High Fructose Corn Syrup']
features = ['No Pulp']

#assess counts from lists above for their presence in query_df  
assessed_query = assess_query(query_df, prioritize, avoid, features)

#filter assessed_query so that it only contains perfect matches
perfect_matches = perfect_match(assessed_query, prioritize, avoid, features)

#convert perfect matches to graph dict
graph_dict = ...

#generate position dict from graph dict
position_dict = ...

#plot network graph 







