"""
No support for
 - numerical annotation rows
 - multi-numeric rows
"""
from perseuspy import dependent_peptides
import perseuspy.io.maxquant
from perseuspy.io.perseus import to_perseus, read_perseus
# Monkey-patching pandas
import pandas as pd
pd.DataFrame.to_perseus = to_perseus
pd.read_perseus = read_perseus

