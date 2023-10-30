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



#read in dataframe from parsed_branded.csv
df = pd.read_csv("C:\\Users\\16185\\Desktop\\parsed_branded_food.csv")

#test Orange Juice Query and Display
search_str = 'Orange Juice'
prioritize = ['Organic']
avoid = ['Sugar', 'Sodium Benzoate', 'High Fructose Corn Syrup']
features = ['Pulp Free']

display_perfect_matches(df, search_str, prioritize, avoid, features)






