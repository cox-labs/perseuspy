import numpy as np
import pandas as pd
from collections import OrderedDict

separator = '\t'
def multi_numeric_converter(numbers):
    return [float(num) for num in numbers.split(';') if num != '']

converters = {'M': multi_numeric_converter}

perseus_to_dtype = {'E' : float, 'T' : str, 'C' : 'category', 'N' : float}

def dtype_to_perseus(dtype):
    if type(dtype) is pd.core.dtypes.dtypes.CategoricalDtype:
        return 'C'
    else:
        mapping = {np.dtype('float'): 'N', np.dtype('str'): 'T',
                   np.dtype('object'): 'T', np.dtype('int64'): 'N',
                   np.dtype('bool'): 'C'}
        return mapping[dtype]

def read_annotations(path_or_file, separator='\t', reset=True):
    """
    Read all annotations from the specified file.
    
    >>> annotations = read_annotations(path_or_file, separator)
    >>> colnames = annotations['Column Name']
    >>> types = annotations['Type']
    >>> annot_row = annotations['Annot. row name']

    :param path_or_file: Path or file-like object
    :param separator: Column separator
    :param reset: Reset the file after reading. Useful for file-like, no-op for paths.
    :returns: Ordered dictionary of annotations.
    """
    annotations = OrderedDict({})
    with PathOrFile(path_or_file, 'r', reset=reset) as f:
        annotations['Column Name'] = f.readline().strip().split(separator)
        for line in f:
            if line.startswith('#!{'):
                tokens = line.strip().split(separator)
                _name, first_value = tokens[0].split('}')
                name = _name.replace('#!{', '')
                values = [first_value] + tokens[1:]
                if name == 'Type':
                    colnames = annotations['Column Name']
                    annotations['dtype'] = {colnames[i]: perseus_to_dtype[x] for i, x in enumerate(values) if x in perseus_to_dtype}
                    annotations['converters'] = {colnames[i]: converters[x] for i, x in enumerate(values) if x in converters}
                annotations[name] = values
    return annotations

def annotation_rows(prefix, annotations):
    """
    Helper function to extract N: and C: rows from annotations and pad their values
    """
    ncol = len(annotations['Column Name'])
    return {name.replace(prefix, '', 1) : values + [''] * (ncol - len(values))
            for name, values in annotations.items() if name.startswith(prefix)}


def create_column_index(annotations):
    """
    Create a pd.MultiIndex using the column names and any categorical rows.
    Note that also non-main columns will be assigned a default category ''.
    """
    _column_index = OrderedDict({'Column Name' : annotations['Column Name']})
    categorical_rows = annotation_rows('C:', annotations)
    _column_index.update(categorical_rows)
    numerical_rows = {name: [float(x) if x != '' else float('NaN') for x in values]
            for name, values in annotation_rows('N:', annotations).items()} # to floats
    _column_index.update(numerical_rows)
    column_index = pd.MultiIndex.from_tuples(list(zip(*_column_index.values())), names=list(_column_index.keys()))
    if len(column_index.names) == 1:
        # flatten single-level index
        name = column_index.names[0]
        column_index = column_index.get_level_values(name)
    return column_index

def read_perseus(path_or_file, **kwargs):
    """
    Read a Perseus-formatted matrix into a pd.DataFrame.
    Annotation rows will be converted into a multi-index.

    By monkey-patching the returned pd.DataFrame a `to_perseus`
    method for exporting the pd.DataFrame is made available.

    :param path_or_file: File path or file-like object
    :param kwargs: Keyword arguments passed as-is to pandas.read_csv
    :returns: The parsed data frame
    """
    annotations = read_annotations(path_or_file, separator)
    column_index = create_column_index(annotations)
    if 'usecols' in kwargs:
	    usecols = kwargs['usecols']
	    if type(usecols[0]) is str:
		    usecols = sorted([list(column_index).index(x) for x in usecols])
	    column_index = column_index[usecols]
    kwargs['dtype'] = dict(kwargs.get('dtype', {}), **annotations.get('dtype', {}))
    kwargs['converters'] = dict(kwargs.get('converters', {}), **annotations.get('converters', {}))
    df = pd.read_csv(path_or_file, sep=separator, comment='#', **kwargs)
    df.columns = column_index
    return df

import numpy as np
def to_perseus(df, path_or_file, main_columns=None,
        separator=separator,
        convert_bool_to_category=True,
        numerical_annotation_rows = set([])):
    """
    Save pd.DataFrame to Perseus text format.

    :param df: pd.DataFrame.
    :param path_or_file: File name or file-like object.
    :param main_columns: Main columns. Will be infered if set to None. All numeric columns up-until the first non-numeric column are considered main columns.
    :param separator: For separating fields, default='\t'.
    :param covert_bool_to_category: Convert bool columns of True/False to category columns '+'/'', default=True.
    :param numerical_annotation_rows: Set of column names to be interpreted as numerical annotation rows, default=set([]).
    """
    _df = df.copy()
    if not _df.columns.name:
        _df.columns.name = 'Column Name'
    column_names = _df.columns.get_level_values('Column Name')
    annotations = {}
    main_columns = _infer_main_columns(_df) if main_columns is None else main_columns
    annotations['Type'] = ['E' if column_names[i] in main_columns else dtype_to_perseus(dtype)
            for i, dtype in enumerate(_df.dtypes)]
    # detect multi-numeric columns
    for i, column in enumerate(_df.columns):
        valid_values = [value for value in _df[column] if value is not None]
        if len(valid_values) > 0 and all(type(value) is list for value in valid_values):
            annotations['Type'][i] = 'M'
            _df[column] = _df[column].apply(lambda xs: ';'.join(str(x) for x in xs))
    if convert_bool_to_category:
        for i, column in enumerate(_df.columns):
            if _df.dtypes[i] is np.dtype('bool'):
                values = _df[column].values
                _df[column][values] = '+'
                _df[column][~values] = ''
    annotation_row_names = set(_df.columns.names) - {'Column Name'}
    for name in annotation_row_names:
        annotation_type = 'N' if name in numerical_annotation_rows else 'C'
        annotations['{}:{}'.format(annotation_type, name)] = _df.columns.get_level_values(name)
    with PathOrFile(path_or_file, 'w') as f:
        f.write(separator.join(column_names) + '\n')
        for name, values in annotations.items():
            f.write('#!{{{name}}}{values}\n'.format(name=name, values=separator.join([str(x) for x in values])))
        _df.to_csv(f, header=None, index=False, sep=separator)

class PathOrFile():
    """Small context manager for file paths or file-like objects
    :param path_or_file: Path to a file or file-like object
    :param mode: Set reading/writing mode
    :param reset: Reset file-like to initial position. Has no effect on path."""
    def __init__(self, path_or_file, mode = None, reset=False):
        self.path_or_file = path_or_file
        self.mode = mode
        self.isPath = isinstance(path_or_file, str)
        self.reset = reset and not self.isPath
        if self.reset:
            self.position = self.path_or_file.seek(0, 1)

    def __enter__(self):
        if self.isPath:
            self.open_file = open(self.path_or_file, self.mode)
            return self.open_file
        else:
            self.open_file = None
            return self.path_or_file

    def __exit__(self, *args):
        if self.open_file:
            self.open_file.close()
        if self.reset:
            self.path_or_file.seek(self.position)

_numeric_dtypes = {np.dtype('float32'), np.dtype('float64'), np.dtype('int32'), np.dtype('int64')}
def _infer_main_columns(df, index_level='Column Name', numeric_dtypes=_numeric_dtypes):
    """
    All numeric columns up-until the first non-numeric column are considered main columns.
    :param df: The pd.DataFrame
    :param index_level: Name of the index level of the column names. Default 'Column Name'
    :param numeric_dtypes: Set of numpy.dtype containing all numeric types. Default int/float.
    :returns: The names of the infered main columns
    """
    columns = df.columns.get_level_values(index_level)
    main_columns = []
    for i,dtype in enumerate(df.dtypes):
        if dtype in numeric_dtypes:
            main_columns.append(columns[i])
        else:
            break
    return main_columns

def main_df(infile, df):
    annotations = read_annotations(infile)
    main_index = []
    i = 0
    for c_type in annotations['Type']:
        if c_type == 'E':
            main_index.append(i)
        i = i + 1
    main_dataframe = df.ix[:, main_index[0]:main_index[-1]+1]
    return main_dataframe
