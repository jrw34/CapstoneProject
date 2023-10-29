from ingredient_parser import*
import pandas as pd
import re
import numpy as np


#import data
branded_food = pd.read_csv("C:\\Users\\16185\\Desktop\\branded apr 2023\\branded_food.csv", low_memory=False)

category_map_table = pd.read_excel("C:\\Users\\16185\\Desktop\\food_categories (1).xlsx")

food = pd.read_csv("C:\\Users\\16185\\Desktop\\branded apr 2023\\food.csv")

category_map = {}
for k,v in dict(zip(category_map_table['category_name'][:], category_map_table['map_key'][:])).items():
	category_map[str(k).strip()] = str(v).strip()

df = branded_food.merge(food, on='fdc_id')

df['category_group'] = df['branded_food_category'].map(category_map)

df['ingred_list'] = df.ingredients.apply(lambda x: ingredient_parser(x, comma_tags, empty_tags))

new_df = df.copy().dropna(axis = 0, subset='description')

new_df.loc[:, 'description'] = new_df.loc[:,'description'].apply(lambda x: str(x).upper())


#export new_df to a csv file located on my desktop
new_df.to_csv("C:\\Users\\16185\\Desktop")

