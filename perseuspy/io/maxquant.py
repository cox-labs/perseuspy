"""
utility functions for parsing various generic output tables
of MaxQuant/Perseus
"""
import pandas as pd
from os import path

def read_rawFilesTable(filename):
    """parse the 'rawFilesTable.txt' file into a pandas dataframe"""
    exp = pd.read_table(filename)
    expected_columns = ['File', 'Exists', 'Size', 'Data format', 'Parameter group', 'Experiment', 'Fraction']
    if len(exp.columns) != len(expected_columns) or list(exp.columns) != expected_columns:
        message = '\n'.join(['The raw files table has the wrong format!',
            'It should contain columns:',
            ', '.join(expected_columns),
            'Found columns:',
            ', '.join(exp.columns)])
        raise ValueError(message)
    exp['Raw file'] = exp['File'].apply(path.basename).apply(path.splitext).str.get(0)
    return exp
