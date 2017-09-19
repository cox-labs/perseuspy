"""
perseuspy module for Python-Perseus interop.

Currently there is no support for the following Perseus matrix features:
 - numerical annotation rows
 - multi-numeric rows
"""
__version__ = '0.2.0'
import perseuspy.dependent_peptides
import perseuspy.io.perseus.matrix
# Monkey-patching pandas
import pandas as pd
pd.DataFrame.to_perseus = perseuspy.io.perseus.matrix.to_perseus
pd.read_perseus = perseuspy.io.perseus.matrix.read_perseus

import perseuspy.io.perseus.network
from perseuspy.io.perseus.network import read_networks, write_networks
import networkx as nx
nx.from_perseus = perseuspy.io.perseus.network.from_perseus
nx.to_perseus = perseuspy.io.perseus.network.to_perseus
try:
    pass
except ImportError as e: # this shold happen only during installation
    print(e)
