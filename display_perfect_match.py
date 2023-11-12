from ingredient_request import* 
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from collections import Counter


def perfect_match_to_graph_dict(df, prioritize, avoid, features):
    """Returns a dictionary from a dataframe that can be transformed into a plotly network graph"""
    
    matched_brands = df.brand_owner.unique()
    my_graph_dict = {brand : {} for brand in matched_brands}

    for brand in matched_brands:
        single_brand_group = pd.DataFrame(df.groupby('brand_owner').get_group(brand))
        for idx, row in single_brand_group.iterrows():
            if row['brand_owner'] in my_graph_dict:
                my_graph_dict[row['brand_owner']][row['description']] = row['ingred_list']

    return my_graph_dict



#def graph_display functionality
def dict_to_position_dict(graph_dict):
    """Returns a dictionary of index : node_information_tuple for each item in graph_dict"""
    
    num_brands = len(graph_dict)

    num_nodes = sum([2 for brand in graph_dict for description in graph_dict[brand]]) + num_brands
    
    full_pos_dict = {j : () for j in range(num_nodes)}
    dict_index_counter = 0

    #add position for each brand node
    for idx,brand in enumerate(graph_dict):
        full_pos_dict[dict_index_counter] = ((num_brands**2)*(2*num_brands * idx), 20, brand)
        dict_index_counter += 1
    
        brand_dict = graph_dict[brand]
        #add position for each description node
        for sub_idx, description in enumerate(brand_dict):
            
            #if only one child then stack directly below, else use alternating shift (e.g. -1, 1) 
            if len(brand_dict) == 1:
                full_pos_dict[dict_index_counter] = ((num_brands**2)*(2*num_brands * idx), 
                                                     (-1)**(idx)+idx + 5, 
                                                     description)
                
                dict_index_counter += 1
            
                #place ingredient as as child node of the description
                full_pos_dict[dict_index_counter] = ((num_brands**2)*(2*num_brands * idx), 
                                                     (-1)**(idx)+idx -5, 
                                                     brand_dict[description])
                
                dict_index_counter += 1
            
            else:
                full_pos_dict[dict_index_counter] = ((num_brands**2)*(2*num_brands * idx)+((-1)**(sub_idx)*8)+idx, 
                                                     (-1)**(sub_idx), 
                                                     description)
                
                dict_index_counter += 1
            
                full_pos_dict[dict_index_counter] = ((num_brands**2)*(2*num_brands * idx)+((-1)**(sub_idx)*8)+idx, 
                                                     (-1)**(sub_idx) - 7, 
                                                     brand_dict[description])
                
                dict_index_counter += 1
    
    return full_pos_dict



def range_list_constructor(graph_dict):
    """Returns a list of range(start, stop+1) for start = index_brand_start, stop = index_brand_end for each brand"""
    
    brand_network_sizes = {brand : 2*len(graph_dict[brand])+1 for brand in graph_dict}
    
    brands_list = list(brand_network_sizes)
    
    brand_network_ranges = {}
    
    rolling_sum = [0]
    for i in range(len(brands_list)):
        rolling_sum.append(rolling_sum[i]+brand_network_sizes[brands_list[i]])
        
    return [range(rolling_sum[i-1],rolling_sum[i]) for i in range(1,len(rolling_sum))]



def node_generator(position_dict, brand_range_list):
    """Returns corresponding list for x positions, y positions, and text for each: brand, description, ingredient"""
    brand_x, brand_y, brand_text = [], [], []
    desc_x, desc_y, desc_text = [], [], []
    ingred_x, ingred_y, ingred_text = [], [], []
    
    for rng in brand_range_list:
        
        #if first element in range even then all ingredients are even and all descriptions odd
        if rng[0] % 2 == 0:
            #convert to list to grant mutability
            temp_list = list(rng)
            #data structure ensures first element in the range is associated with the brand
            brand_loc = temp_list.pop(0)
            brand_x.append(position_dict[brand_loc][0])
            brand_y.append(position_dict[brand_loc][1])
            brand_text.append(position_dict[brand_loc][2])
            #for rest of indices in range append to either description(odd) or ingredients(even)
            for r in temp_list:
                if r % 2 == 1:
                    desc_x.append(position_dict[r][0])
                    desc_y.append(position_dict[r][1])
                    desc_text.append(position_dict[r][2])
                else:
                    ingred_x.append(position_dict[r][0])
                    ingred_y.append(position_dict[r][1])
                    ingred_text.append(position_dict[r][2])
        
        else:
            temp_list = list(rng)
            #data structure ensures first element in the range is associated with the brand
            brand_loc = temp_list.pop(0)
            brand_x.append(position_dict[brand_loc][0])
            brand_y.append(position_dict[brand_loc][1])
            brand_text.append(position_dict[brand_loc][2])
            #for rest of indices in range append to either description(even) or ingredients(odd)
            for r in temp_list:
                if r % 2 == 0:
                    desc_x.append(position_dict[r][0])
                    desc_y.append(position_dict[r][1])
                    desc_text.append(position_dict[r][2])
                else:
                    ingred_x.append(position_dict[r][0])
                    ingred_y.append(position_dict[r][1])
                    ingred_text.append(position_dict[r][2])
                    
                    
    return brand_x, brand_y, brand_text, desc_x, desc_y, desc_text, ingred_x, ingred_y, ingred_text



def edge_index_zipper(graph_dict):
    """Returns zipped list of brand indices mapping to their respective description"""
    parent_child_idx_map = {i : [] for i in range(0, len(graph_dict))}
    
    parent_idx, child_idx = 0, 0
    for k,v in graph_dict.items():
        for k2, v2 in v.items():
            parent_child_idx_map[parent_idx].append(child_idx)
            child_idx += 1
        parent_idx += 1
        
    parent_idx_list, child_idx_list = [], []
    for k,v in parent_child_idx_map.items():
        parent_idx_list.append([k]*len(v))
        child_idx_list.append(v)
    
    #return flattened lists zipped together
    return zip([i for j in parent_idx_list for i in j], [k for l in child_idx_list for k in l])



def plot_network_digraph(brand_x, brand_y, brand_text, desc_x, desc_y, desc_text, ingred_x, ingred_y, ingred_text, graph_dict, Search_String):
    """Plots an interactive directed network graph for the graph_dict transformed by the functions listed below"""
    """
    Required Functions: dict_to_position_dict
                        range_list_constructor
                        edge_index_zipper
                        node_generator --> this should be the input for the function
    
    Expected input: *node_generator(position_dict, brand_range_list), graph_dict
    """
    brand_desc_zipped_indices = edge_index_zipper(graph_dict)
    
    brand_trace = go.Scatter(
                    name = 'Brand Onwer',
                    x=brand_x,
                    y=brand_y,
                    mode='text',
                    text = brand_text,
                    textposition='top center',
                    hovertemplate = brand_text,
                    textfont=dict(
                                color="white"
                                 )
                            )
    
    description_trace = go.Scatter(
                          name = 'Description',
                          x=desc_x,
                          y=desc_y,
                          mode='markers',
                          marker_size=12,
                          marker_symbol = 'square',
                          hovertemplate = desc_text,
                          textfont=dict(
                                color="white"
                                 )
                                  )
    
    ingredient_trace = go.Scatter(
                          name = 'Ingredients',
                          x=ingred_x,
                          y=ingred_y,
                          mode='markers',
                          marker_size=12,
                          hovertemplate = ingred_text,
                          textfont=dict(
                                color="white"
                                 )
                          
                                  )
    
    #create list_of_all_arrows
    list_of_desc_edges = []
    for i,j in zip(range(0,len(desc_x)), range(0, len(desc_x))): 
        edge = go.layout.Annotation(dict(
                                    ax = desc_x[i],
                                    ay = desc_y[i],
                                    axref='x',
                                    ayref='y',
                                    x=ingred_x[j],
                                    y=ingred_y[j],
                                    xref='x',
                                    yref='y',
                                    arrowwidth=2,
                                    arrowcolor='silver',
                                    arrowsize=0.6,
                                    opacity=0.3,
                                    showarrow=True,
                                    arrowhead=1))
        
        list_of_desc_edges.append(edge)

    list_of_brand_edges = []
    for i,j in brand_desc_zipped_indices:
        edge = go.layout.Annotation(dict(
                                ax = brand_x[i],
                                ay = brand_y[i],
                                axref='x',
                                ayref='y',
                                x=desc_x[j],
                                y=desc_y[j],
                                xref='x',
                                yref='y',
                                arrowwidth=2,
                                arrowcolor='silver',
                                arrowsize=0.6,
                                opacity=0.3,
                                showarrow=True,
                                arrowhead=1,))
        
        list_of_brand_edges.append(edge)


    list_of_all_edges = list_of_brand_edges + list_of_desc_edges
    
    fig = go.Figure(data = [brand_trace,
                            description_trace,
                            ingredient_trace],
                    layout=go.Layout(
                            height=1000,
                            width=1000,
                            title=f'All Perfect Matches For {Search_String}',
                            annotations = list_of_all_edges))
                       
                                       
                                
                
    
    
    min_x = min(ingred_x)
    max_x = max(ingred_x)
    fig.update_xaxes(range=[min_x-50,max_x+50],showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_layout(plot_bgcolor='darkblue')
    
    
    fig.show()



def plot_query_network(graph_dict, Search_String):
    """Takes a dict_of_dicts as input and returns an interactive digraph for each key,dict pair in the dict_of_dicts"""
    
    
    #convert to position dict of node : 3-tuples
    position_dict = dict_to_position_dict(graph_dict)
    
    #generate list of ranges for each brand in position_dict
    brand_range_list = range_list_constructor(graph_dict)
    
    #information required for plotly network graph is created by node_generator(position_dict, brand_range_dict)
    """
    brand_x, brand_y, brand_text,
    desc_x, desc_y, desc_text, 
    ingred_x, ingred_y, ingred_text = node_generator(position_dict, brand_range_dict)
    """
    
    return plot_network_digraph(*node_generator(position_dict, brand_range_list), graph_dict, Search_String)



#use all functions defined above together to display a network graph of the perfect matches
def display_perfect_matches(df, search_item, prioritize, avoid, features):
    """Returns a plotly network digraph for a specified query on the dataframe"""
    """
    Required Input:
                    df: A cleaned dataframe containing non null columns
                    prioritize: A list of ingredients/qualities you want the item to contain
                    avoid: A list of ingredients/qualities you do not want the item to contain
                    features: A list of features associated with the item description that you want like 'No pulp'
    """
    
    
    prioritize = [p.upper() for p in prioritize]
    avoid = [a.upper() for a in avoid]
    features = [f.upper() for f in features]
    
    queried_graph_dict = perfect_match_to_graph_dict(df, prioritize, avoid, features)
    
    return plot_query_network(queried_graph_dict, search_item)