import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import plotly.graph_objs as go

#compile all re expressions for ingredient parsing 


contains_re = re.compile(r"CONTAIN[S|:]?\+?[ING]*")

less_than_re = re.compile(r"LESS THAN [0-9|\.{0,3}]*%?\s?:?(EACH|OF)?:?")

pct_or_less_re = re.compile(r"[0-9|.]{0,3}\%?\s?(OR)?\sLESS (OF:?)?")

#remove all statements relating to additives or contents
def additive_tag_substitution(input_str, contains_re, less_than_re, pct_or_less_re):
    """Takes a string of ingredients and removes contents of string identified in CONTENTS.txt"""
    
    """
    Required input: 3 compiled regex expresssions
        1) contains_re: r"CONTAIN[S|:]?\+?[ING]*"
        2) less_than_re: r"LESS THAN [0-9|\.{0,3}]*%?\s?:?(EACH|OF)?:?"
        3) pct_or_less_re: r"[0-9|.]{0,3}\%?\s?(OR)?\sLESS (OF:?)?"
    """

    #sub contains
    sub1 = re.sub(contains_re, " ", input_str)
    
    #sub less than
    sub2 = re.sub(less_than_re, " ", sub1)
    
    #sub pct or less
    sub3 = re.sub(pct_or_less_re, " ", sub2)
    
    return sub3



#create list of strings to be replaced with ','
comma_tags = [".CONTAINS:", " - ", " (", ")" ," [", "]", " {", "}"]

#create list of strings to be replaced with ''
empty_tags = ["INGREDIENTS:"," FOR COLOR", "*", 
              "CONSISTS OF","CONSIST OF", "ONE OR MORE OF THE FOLLOWING", 
              "OF THE FOLLOWING", "THE FOLLOWING", "PRESERVATIVES", 
              "AS A PRESERVATIVE", "FOR TARTNESS", "TO PRESERVE FRESHNESS",
             "TO PREVENT CAKING", "ANTI-CAKING AGENT", "ANTICAKING AGENT", 
              "FOR COLOR", "COLOR ADDED", "EACH", 
              "PRESERVATIVE", "USED FOR", "USED AS A", 
              "USED"]


#def ingredient_parser function to operate on ingredients column of branded_food.csv
def ingredient_parser(input_str, comma_tags, empty_tags):
    """Returns a list of cleaned food ingredients from a single ingredient string"""
    
    
    #normalize input_str
    normed_str = str(input_str).upper()
    
    #convert "PERCENT" to "%"
    normed_str = normed_str.replace(" PERCENT", "%")
    
    #replace substrings with ""
    for tag in empty_tags:
        normed_str = normed_str.replace(tag, "")
    
    #replace substrings with ","
    for tag in comma_tags:
        normed_str = normed_str.replace(tag, ",")
    
    #remove pieces describes in CONTAINS_REMOVAL.TXT
    normed_str = additive_tag_substitution(normed_str, contains_re, less_than_re, pct_or_less_re)
    
    #sparse colon and semicolon replacement
    normed_str = normed_str.replace(":", ",").replace(";", ",")
    
    return [i.strip().rstrip('.') for i in normed_str.split(",") if i.strip().rstrip('.') != '']


