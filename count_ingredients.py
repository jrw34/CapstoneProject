import pandas as pd 
import numpy as np
from collections import Counter
from itertools import combinations
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def get_ingredient_counts(df, max_ngram):
    
    """Returns counts of each ingredient and n-combinations of ingredients from a df produced by description_query_db function"""
    
    ingredients_series = df['ingred_list']
    cleaned_ingredients = ingredients_series.apply(lambda x: x.strip('{').strip('}').replace('"', ''))
    all_ingredients = pd.Series((i for x in cleaned_ingredients for i in x.split(',') if i != ''))
    
    count_container = dict()
    
    
    while max_ngram > 1:
        
        temp_n_gram = cleaned_ingredients.apply(lambda x: list(combinations(x.split(','), max_ngram))
                                                               if len(x.split(',')) > max_ngram and ',' in x and len(x) > 1 else x)
        
        temp_flat = [i for t in temp_n_gram for i in t]
        
        counted_ngram = Counter(temp_flat)
        
        #compute third quartile to filter out majority of results to display
        temp_q9 = np.percentile(np.array([i for i in counted_ngram.values()]), 90)
        
        temp_len = len(counted_ngram)
        counted_temp = {str(k) : int(v)/temp_len for k,v in counted_ngram.items() if v > temp_q9}
        
        count_container[max_ngram] = counted_temp
        
        max_ngram -= 1
        
    
    counted_one_gram = Counter(list(all_ingredients))
    
    q9 = np.percentile(np.array([i for i in counted_one_gram.values()]), 90)
    
    one_gram_len = len(counted_one_gram)
    
    counted_one = {str(k) : int(v)/one_gram_len for k,v in counted_one_gram.items() if v > q9}
    
    count_container[max_ngram] = counted_one
    
    
    return count_container    


def plot_ingredient_counts(count_container):
    
    single_ingredient_counts = count_container[1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x= [c for c in single_ingredient_counts.values()],
                         y= [i for i in single_ingredient_counts.keys()],
                         orientation = 'h',
                         name='Most Common (Top 10%) Ingredients',
                         marker_color='blue',
                        )
                 )
    
    paired_ingredient_counts = count_container[2]
    
    fig.add_trace(go.Bar(x = [c for c in paired_ingredient_counts.values() ],
                         y = [i for i in paired_ingredient_counts.keys()   ],
                         orientation = 'h',
                         marker_color = 'green',
                         name = 'Most Common (Top 10%) Ingredient Pairs'
                        )
                 )
                         
                         
    return fig
    