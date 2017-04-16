"""
utility functions for parsing various generic output tables
of MaxQuant/Perseus
"""
import pandas as pd
from os import path

def read_experimentalDesign(filename):
    """parse the 'experimentalDesign.txt' file into a pandas dataframe"""
    exp = pd.read_table(filename)
    exp['Raw file'] = exp['File'].apply(path.basename).apply(path.splitext).str.get(0)
    return exp
