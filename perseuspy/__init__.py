"""
No support for
 - numerical annotation rows
 - multi-numeric rows
"""
import numpy as np
import pandas as pd
from collections import OrderedDict

separator = '\t'
perseus_to_dtype = {'E' : float, 'T' : str, 'C' : 'category', 'M' : str, 'N' : float}
dtype_to_perseus = { np.dtype('float') : 'N', np.dtype('str') : 'T', np.dtype('object') : 'T',
        pd.Categorical.dtype : 'C' }

def read_annotations(filename, separator, type_map=perseus_to_dtype):
    """
    Read all annotations from the specified file.
    
    >>> annotations = read_annotations(filename, separator)
    >>> colnames = annotations['Column Name']
    >>> types = annotations['Type']
    >>> annot_row = annotations['Annot. row name']
    """
    annotations = OrderedDict({})
    with open(filename) as f:
        annotations['Column Name'] = f.readline().strip().split(separator)
        for line in f:
            if line.startswith('#!{'):
                tokens = line.strip().split(separator)
                _name, first_value = tokens[0].split('}')
                name = _name.replace('#!{', '')
                values = [first_value] + tokens[1:]
                if name == 'Type':
                    values = [type_map[x] for x in values]
                annotations[name] = values
    return annotations

def create_column_index(annotations):
    """
    Create a pd.MultiIndex using the column names and any categorical rows.
    Note that also non-main columns will be assigned a default category ''.
    """
    _column_index = OrderedDict({'Column Name' : annotations['Column Name']})
    ncol = len(_column_index['Column Name'])
    categorical_rows = {name.replace('C:','',1) : values + [''] * (ncol - len(values)) for name, values in annotations.items() if name.startswith('C:')}
    _column_index.update(categorical_rows)
    column_index = pd.MultiIndex.from_tuples(list(zip(*_column_index.values())), names=_column_index.keys())
    return column_index

def read_perseus(filename, type_map = perseus_to_dtype):
    """
    Read a Perseus-formatted matrix into a pd.DataFrame.
    Annotation rows will be converted into a multi-index.

    By monkey-patching the returned pd.DataFrame a `to_perseus`
    method for exporting the pd.DataFrame is made available.
    """
    annotations = read_annotations(filename, separator, type_map)
    column_index = create_column_index(annotations)
    dtype = {name : t for name, t in zip(annotations['Column Name'], annotations['Type'])}
    df = pd.read_csv(filename, sep=separator, comment='#', dtype = dtype)
    df.columns = column_index
    return df

import numpy as np
def to_perseus(df, filename, main_columns=None, separator=separator, type_map = dtype_to_perseus):
    """
    Save pd.DataFrame to Perseus text format.

    :param df: pd.DataFrame
    :param filename: File name
    :param main_columns: Main columns. Will be infered if set to None. All numeric columns up-until the first non-numeric column are considered main columns.
    :param separator: For separating fields, default '\t'
    """
    column_names = df.columns.get_level_values('Column Name')
    annotations = {}
    main_columns = _infer_main_columns(df) if main_columns is None else main_columns
    annotations['Type'] = ['E' if i in main_columns else type_map[dtype] for i, dtype in enumerate(df.dtypes)]
    annotation_row_names = set(df.columns.names) - {'Column Name'}
    for name in annotation_row_names:
        annotations['C:{}'.format(name)] = df.columns.get_level_values(name)
    with open(filename, 'w') as f:
        f.write(separator.join(column_names) + '\n')
        for name, values in annotations.items():
            f.write('#!{{{name}}}{values}\n'.format(name=name, values=separator.join(values)))
        df.to_csv(f, header=None, index=False, sep=separator)

def _infer_main_columns(df):
    """
    All numeric columns up-until the first non-numeric column are considered main columns.
    """
    main_columns = []
    for i,dtype in enumerate(df.dtypes):
        if dtype in {np.dtype('float'), np.dtype('int')}:
            main_columns.append(i)
        else:
            break
    return main_columns

# Monkey-patching pandas
pd.DataFrame.to_perseus = to_perseus
pd.read_perseus = read_perseus

