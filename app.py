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

    search_str = 'Orange Juice'.upper()
    query_df = description_query_db(search_str)
    
    prioritize = ['Organic'.upper()]
    avoid = ['Sodium Benzoate'.upper(), 'HIGH FRUCTOSE CORN SYRUP']
    features = ['No Pulp'.upper()]
    
    assessed_query = assess_query(query_df, prioritize, avoid, features)
    
    perfect_matches = perfect_match_from_assessed(assessed_query, prioritize, avoid, features)
    
    st.plotly_chart(display_perfect_matches(perfect_matches, search_str, prioritize, avoid, features))


if __name__ == "__main__":
    app()
