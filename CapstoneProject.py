import pandas as pd 
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter
from ingredient_parser import*
from ingredient_query import*
from display_perfect_match import*



#read data from 'branded_food.csv'
data = pd.read_csv("C:\\Users\\16185\\Desktop\\branded apr 2023\\branded_food.csv", low_memory=False)

#read data from 'food.csv' to merge with data to include 'food_category_id'
category_data = pd.read_csv("C:\\Users\\16185\\Desktop\\branded apr 2023\\food.csv")

#merge columns to that category_id is included in the dataframe for analysis/modelling
df = data.merge(right = category_data, on = 'fdc_id')


#create ingred_list column containing sets of parsed ingredients
df['ingred_list'] = df.ingredients.apply(lambda x: ingredient_parser(x, comma_tags, empty_tags))

#drop all rows where 'description' is nan
df_dropped = df.dropna(axis = 0, subset = 'description')


#test Orange Juice Query and Display
search_str = 'Orange Juice'
prioritize = ['Organic']
avoid = ['Sugar', 'Sodium Benzoate', 'High Fructose Corn Syrup']
features = ['Pulp Free']

display_perfect_matches(df_dropped, search_str, prioritize, avoid, features)






