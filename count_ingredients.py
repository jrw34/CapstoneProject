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
        
        temp_flat = [i for t in temp_n_gram for i in t if len(i) > 3]
        
        counted_ngram = Counter(temp_flat)
        
        top_25 = counted_ngram.most_common(25)
        
        top_25_counts = { str(k[0]) : int(k[1]) for k in top_25 }  
        
        count_container[max_ngram] = top_25_counts
        
        max_ngram -= 1
        
    
    counted_one_gram = Counter(list(all_ingredients))
    
    q9 = np.percentile(np.array([i for i in counted_one_gram.values()]), 90)
    
    one_gram_len = len(counted_one_gram)
    
    counted_one = {str(k) : int(v) for k,v in counted_one_gram.items() if v > q9}
    
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
                         name = '25 Most Common Ingredient Pairs'
                        )
                 )
                 
        
    fig.update_layout(title = "Most Common Ingredients")
                         
    return fig
    