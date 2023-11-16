import streamlit as st
import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter
from sqlalchemy import create_engine, text
import os

from ingredient_request import*
from display_perfect_match import*
from description_query import*


def app():
    st.title("Find the food products that you want to eat!")

    search_str = st.text_input('What Item are you looking for? Try something like Orange Juice or Whole Grain Bread')
    query_df = description_query_db(search_str.upper())
    
    preference = st.text_input('What are your preferences? Try something like Organic or Gluten Free')
    prioritize = preference.upper()
    
    features = ['No Pulp'.upper()]
    
    reformatted_ingredients = query_df.ingred_list.apply(lambda x: x.strip('{').strip('}').replace('"', ''))
    all_ingredients = set([i for x in reformatted_ingredients for i in x.split(',') if i != ''])
    
    
    
    with st.form("Preferences and Ingredients to Avoid"):
        
        
        avoid = st.multiselect("What ingredients do you want to avoid? Maybe try Enriched Wheat Flour or Sodium Benzoate",
                            all_ingredients)
          
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            assessed_query = assess_query(query_df, prioritize, avoid, features)
            perfect_matches = perfect_match_from_assessed(assessed_query, prioritize, avoid, features)
            st.plotly_chart(display_perfect_matches(perfect_matches, search_str, prioritize, avoid, features))
    
    
    


if __name__ == "__main__":
    app()
