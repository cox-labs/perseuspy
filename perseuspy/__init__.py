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
        np.dtype('int64') : 'N', pd.Categorical.dtype : 'C' }

def read_annotations(path_or_file, separator, type_map=perseus_to_dtype):
    """
    Read all annotations from the specified file.
    
    >>> annotations = read_annotations(path_or_file, separator)
    >>> colnames = annotations['Column Name']
    >>> types = annotations['Type']
    >>> annot_row = annotations['Annot. row name']
    """
    annotations = OrderedDict({})
    with PathOrFile(path_or_file, 'r') as f:
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
    column_index = pd.MultiIndex.from_tuples(list(zip(*_column_index.values())), names=list(_column_index.keys()))
    return column_index

def read_perseus(path_or_file, type_map = perseus_to_dtype, **kwargs):
    """
    Read a Perseus-formatted matrix into a pd.DataFrame.
    Annotation rows will be converted into a multi-index.

    By monkey-patching the returned pd.DataFrame a `to_perseus`
    method for exporting the pd.DataFrame is made available.

    :param path_or_file: File path or file-like object
    :param type_map: How to map Perseus types to numpy.dtype
    :param **kwargs: Keyword arguments passed as-is to pandas.read_csv
    :returns: The parsed data frame
    """
    annotations = read_annotations(path_or_file, separator, type_map)
    column_index = create_column_index(annotations)
    if 'Type' in annotations:
        dtype = {name : t for name, t in zip(annotations['Column Name'], annotations['Type'])}
        df = pd.read_csv(path_or_file, sep=separator, comment='#', dtype = dtype, **kwargs)
    else:
        df = pd.read_csv(path_or_file, sep=separator, comment='#', **kwargs)
    df.columns = column_index
    return df

import numpy as np
def to_perseus(df, path_or_file, main_columns=None,
        separator=separator, type_map = dtype_to_perseus,
        numerical_annotation_columns = set([])):
    """
    Save pd.DataFrame to Perseus text format.

    :param df: pd.DataFrame
    :param path_or_file: File name or file-like object
    :param main_columns: Main columns. Will be infered if set to None. All numeric columns up-until the first non-numeric column are considered main columns.
    :param separator: For separating fields, default '\t'
    """
    column_names = df.columns.get_level_values('Column Name')
    annotations = {}
    main_columns = _infer_main_columns(df) if main_columns is None else main_columns
    annotations['Type'] = ['E' if i in main_columns else type_map[dtype] for i, dtype in enumerate(df.dtypes)]
    annotation_row_names = set(df.columns.names) - {'Column Name'}
    for name in annotation_row_names:
        annotation_type = 'N' if name in numerical_annotation_columns else 'C'
        annotations['{}:{}'.format(annotation_type, name)] = df.columns.get_level_values(name)
    with PathOrFile(path_or_file, 'w') as f:
        f.write(separator.join(column_names) + '\n')
        for name, values in annotations.items():
            f.write('#!{{{name}}}{values}\n'.format(name=name, values=separator.join(values)))
        df.to_csv(f, header=None, index=False, sep=separator)

class PathOrFile():
    """Small context manager for file paths or file-like objects"""
    def __init__(self, path_or_file, mode = None):
        self.path_or_file = path_or_file
        self.mode = mode

    def __enter__(self):
        if isinstance(self.path_or_file, str):
            self.open_file = open(self.path_or_file, self.mode)
            return self.open_file
        else:
            self.open_file = None
            return self.path_or_file

    def __exit__(self, *args):
        if self.open_file:
            self.open_file.close()


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

