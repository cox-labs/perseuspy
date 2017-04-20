"""
Dependent peptides can be extracted from the `allPeptides.txt` table
and are annotated using the `experimentalDesign.txt`.

This code forms the basis for the corresponding Perseus plugin PluginDependentPeptides.
"""
import pandas as pd
from perseuspy.io.perseus import read_perseus
pd.read_perseus = read_perseus
from perseuspy.io.maxquant import read_experimentalDesign
from perseuspy.parameters import fileParam, parse_parameters
import numpy as np

_index_columns = ['DP Proteins', 'DP Base Sequence', 'DP Cluster Index', 'DP Modification']
_cols = ['DP Ratio mod/base', 'Raw file', 'DP AA'] + _index_columns
def read_dependent_peptides(filename):
    """ read the dependent peptides table and extract localiztion information
    :param filename: path to the 'allPeptides.txt' table.
    :returns dep, localization: the dependent peptide table, localization information.
    """
    df = (pd.read_perseus(filename, usecols=_cols)
            .dropna(subset=['DP Ratio mod/base']))
    df['DP Ratio mod/base'] = df['DP Ratio mod/base'].astype(float)
    dep = df.pivot_table('DP Ratio mod/base', index=_index_columns,
                columns='Raw file', aggfunc=np.median)
    localization = _count_localizations(df)
    return dep, localization

def _set_column_names(dep, exp):
    """ rename the columns in the dependent peptides table from
    the raw file to the corresponding {experiment}_{fraction}.
    :param dep: dependent peptides table.
    :param exp: experimental design table.
    """
    colnames = exp['Experiment'] + '_' + exp['Fraction'].astype(str)
    file2col = dict(zip(exp['Raw file'], colnames))
    _dep = dep.rename(columns=file2col)
    _dep.columns.name = 'Column Name'
    return _dep
    
from collections import defaultdict
def count(args):
    """ count occurences in a list of lists
    >>> count([['a','b'],['a']])
    defaultdict(int, {'a' : 2, 'b' : 1})
    """
    counts = defaultdict(int)
    for arg in args:
        for item in arg:
            counts[item] = counts[item] + 1
    return counts

def _count_localizations(df):
    """ count the most likely localization for each depentent peptide.
    :param df: allPeptides.txt table.
    """
    grp = df.groupby(_index_columns)
    counts = grp['DP AA'].apply(lambda x: count(x.str.split(';').values))
    counts.index = counts.index.set_names('DP AA', level=4)
    counts.name = 'DP AA count'
    best_localization = counts.reset_index().groupby(_index_columns).apply(_frequent_localizations)
    return best_localization

def _frequent_localizations(df):
    """ returns the most frequent localization for any dependent peptide.
    In case of ties, preference is given to n-terminal modification which are
    biologically more likely to occur
    :param df: allPeptides.txt table.
    """
    max_count = int(df['DP AA count'].max())
    max_aa = set(df[df['DP AA count'] == max_count]['DP AA'].unique())
    result = {'DP AA max count' : max_count}
    if 'nterm' in max_aa:
        result['DP AA'] = 'nterm'
    else:
        result['DP AA'] = ';'.join(sorted(max_aa))
    return pd.Series(result)

def run_dependent_peptides(paramfile, outfile):
    """ transform a allPeptides.txt and experimentalDesign.txt table
    into the dependentPeptides.txt table written in outfile.
    :param paramfile: Perseus parameters.xml including at least two FileParam
    entries names 'allPeptides.txt' and 'experimentalDesign.txt'.
    :param outfile: Path to the output file
    """
    parameters = parse_parameters(paramfile)
    allPeptides_file = fileParam(parameters, 'allPeptides.txt')
    experimentalDesign_file = fileParam(parameters, 'experimentalDesign.txt')
    _dep, localization = read_dependent_peptides(allPeptides_file)
    exp = read_experimentalDesign(experimentalDesign_file)
    dep = _set_column_names(_dep, exp).reset_index()
    main_columns = list(_dep.columns)
    dep.to_perseus(outfile, main_columns=main_columns)
