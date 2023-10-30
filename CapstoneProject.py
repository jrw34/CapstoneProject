import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter
from ingredient_parser import*
from ingredient_query import*
from display_perfect_match import*
import os
import pickle



#read in dataframe from parsed_branded.pkl
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

with open(desktop + "\\parsed_branded.pkl", 'rb') as f:
    df = pickle.load(f)

#test Orange Juice Query and Display
search_str = 'Orange Juice'
prioritize = ['Organic']
avoid = ['Sugar', 'Sodium Benzoate', 'High Fructose Corn Syrup']
features = ['No Pulp']

display_perfect_matches(df, search_str, prioritize, avoid, features)






