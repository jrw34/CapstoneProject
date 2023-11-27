import streamlit as st
import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter
from sqlalchemy import create_engine, text
import os
import pickle
from itertools import combinations
from collections import Counter
from ingredient_request import*
from display_perfect_match import*
from description_query import*
from count_ingredients import get_ingredient_counts, plot_ingredient_counts

@st.cache_data
def cache_db_query(search_str):
    return web_app_desc_query(search_str.upper())
    
def app():
    st.title("Find the food products that you want to eat!")

    #Accept string input to query database
    search_str = st.text_input('What Item are you looking for? Try something like Orange Juice or Whole Grain Bread')
    
    #query db with user input
    query_df = cache_db_query(search_str)
    
    
    #generate list of unique ingredients in query_df 
    cleaned_ingredients = query_df['ingred_list'].apply(lambda x: x.strip('{').strip('}').replace('"', ''))
    
    unique_ingredients = set((i for x in cleaned_ingredients for i in x.split(',') if i != ''))
    
    #Generate ingredient counts for all ingredients in query_df, count up to 3-gram ingredient associations
    ingredient_counts = get_ingredient_counts(query_df, 2) 
    
    #plot these in an interactive plotly bar chart that has each color the n-grams associated with it
    st.plotly_chart(plot_ingredient_counts(ingredient_counts))
    
    #input form to ensure all input gets registered simultaneously
    with st.form("Preferences, Description, and Ingredients to Avoid"):
        
        preference = st.text_input('What are your preferences? Try something like Organic or Gluten Free')
        prioritize = [preference.upper()]

        #add default of None and ensure network graph funcitonality persists
        description = st.text_input('Specifiy as descriptive quality of the item you want. For orange juice this may be something like No Pulp or Pulp Free')
        features = [description.upper()]
        
        
        avoid = st.multiselect("What ingredients do you want to avoid? Maybe try Enriched Wheat Flour or Sodium Benzoate",
                                unique_ingredients)
        
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
        
            assessed_query = assess_query(query_df, prioritize, avoid, features)
            
            perfect_matches = perfect_match_from_assessed(assessed_query, prioritize, avoid, features)
            
            network_graph = display_perfect_matches(perfect_matches, search_str, prioritize, avoid, features)
            
            st.plotly_chart(network_graph)
    


if __name__ == "__main__":
    app()
