import numpy as np 
import pandas as pd 

#search for given string in df_ex.description
def search_df(my_df, search_for, col):
    """Searches for all rows in dataframe that contain search_str, this function is used for finding products in my_df"""
    search_str = str(search_for).upper()
    return my_df.copy()[my_df[col].str.contains(search_str)]



#function to count prioritized ingredients in your search
def priority_counter(ingred_list, priority_list):
    """Returns a count per item in item_df where the count is number of ingredients that are matched from priority list"""
    return sum((1 for p in priority_list if p in ingred_list))



#function to count ingredients to avoid in search
def avoidance_counter(ingred_list, avoid_list):
    """Returns a count per item in item_df where the count is the number of ingredients matched from avoid list"""
    return sum((1 for a in avoid_list if a in ingred_list))



#function to count features like 'No Pulp' in search
def feature_counter(description, feature_list):
    
    return sum((1 for f in feature_list if f in description))



#def function to filter based off of input
def assess_query(searched_df, prioritize, avoid, features):
    
    """Takes item as input and returns number of brands + items that match the description and ranks according to input."""
    
    """
    Required inputs:
    searched_df     --> DataFrame derived from sqlalchemy query, made from description_query file
    prioritize = [] --> List of ingredients you want to find in the item of your choice from ingredients
    avoid = []      --> List of ingredients you want to avoid from ingredients
    features = []   --> List of items to scan from description
    """
    
    #create priority_counter column and add one for every ingredient_match found in ingred_list and priority
    #apply priority_counter in a lambda function for each ingredient
    searched_df['priority_count'] = searched_df.ingred_list.apply(lambda x: priority_counter(x, prioritize))
    
    #create avoid_counter column and add one for every ingredient_match found in ingred_list and avoid
    searched_df['avoid_count'] = searched_df.ingred_list.apply(lambda x: avoidance_counter(x, avoid))
    
    #feature counter for qualities like 'WITH PULP'
    searched_df['feature_count'] = searched_df.description.apply(lambda x: feature_counter(x, features))
    
    
    return searched_df[['brand_owner', 'description', 'priority_count', 
                        'avoid_count', 'feature_count', 'ingred_list',
                        'serving_size']]


def perfect_match_from_assessed(assessed_df, priorities, avoid, features):
    """Returns a dataframe that only contains rows that perfectly meet criteria of user request"""
    num_p = len(priorities)
    num_a = len(avoid)
    num_f = len(features)
    
    perfectly_matched = assessed_df[ (assessed_df['priority_count'] == num_p) 
                                      &
                                     (assessed_df['feature_count'] == num_f)
                                      & 
                                     (assessed_df['avoid_count'] == 0) ]
    
    return perfectly_matched



#def function to filter only perfectly matched items/brands using output of assess_query
def perfect_match(assessed_df, priorities, avoid, features):
    num_p = len(priorities)
    num_a = len(avoid)
    num_f = len(features)
    
    matched_df = assessed_df[ (assessed_df['priority_count'] == num_p) 
                              &
                              (assessed_df['feature_count'] == num_f)
                              & 
                              (assessed_df['avoid_count'] == 0) ]
    
    return matched_df



