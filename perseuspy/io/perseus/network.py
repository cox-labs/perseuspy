from os import path, makedirs
import uuid
import networkx as nx
from collections import OrderedDict
from perseuspy.io.perseus.matrix import read_perseus
import pandas as pd
import warnings

def read_networks(folder):
    """
    Read perseus network collection folder format
    
    >>> network_table, networks = read_networks(folder)
    
    :param folder: Path to network collection
    :returns: Network table and dictionary with 'name', 'edge_table', and 'node_table' keys.
    """
    network_table = read_perseus(path.join(folder, "networks.txt"))
    networks = {}
    for name, guid in network_table[['Name', 'GUID']].values:
        networks[guid] = {
                'name': name,
                'guid': guid,
                'node_table': read_perseus(path.join(folder, "{}_nodes.txt".format(guid))),
                'edge_table': read_perseus(path.join(folder, "{}_edges.txt".format(guid)))
                }
    return network_table, networks

def from_perseus(network_table, networks):
    """
    Create networkx graph from network tables
    
    >>> from perseuspy import read_networks, nx
    >>> network_table, networks = read_networks(folder)
    >>> graphs = nx.from_perseus(network_table, networks)
    """
    graphs = []
    for guid, graph_attr in zip(network_table['GUID'], network_table.values):
        network = networks[guid]
        edge_table = network['edge_table']
        if edge_table[['Source', 'Target']].duplicated().any():
            warnings.warn('Duplicate edges were found and ignored in network {}'.format(network['name']))
        G = nx.from_pandas_dataframe(edge_table, 'Source', 'Target', True, create_using=nx.DiGraph())
        for attr, value in zip(network_table.columns, graph_attr):
            G.graph[attr] = value
        node_table = network['node_table']
        if node_table['Node'].duplicated().any():
            warnings.warn('Duplicate nodes were found and ignored in network {}'.format(network['name']))
        node_column = node_table['Node']
        for name, attributes in zip(node_column, node_table.values):
            if name not in G:
                G.add_node(name)
            for attr, value in zip(node_table.columns, attributes):
                G.node[name][attr] = value
        graphs.append(G)
    return graphs

def to_perseus(graphs):
    """
    Create a network table and the network dictionary for export to Perseus.
    
    :param graphs: Collection of networkx graphs

    >>> from perseuspy import nx
    >>> G = nx.random_graphs.barabasi_albert_graph(10, 3)
    >>> network_table, networks = nx.to_perseus([G])
    """
    graph_attributes = []
    networks = {}
    for graph in graphs:
        attributes = dict(graph.graph)
        attributes.update({"Name" : attributes.get("Name", attributes.get("name", "networkx graph")),
            "GUID": attributes.get("GUID", str(uuid.uuid4()))})
        graph_attributes.append(attributes)
        edge_table = pd.DataFrame([dict(data, **{"Source": str(f), "Target": str(t)}) for f,t,data in graph.edges(data=True)])
        edge_table.columns.name = "Column Name"
        node_table = pd.DataFrame([dict(data, **{"Node": str(n)}) for n,data in graph.nodes(data=True)])
        node_table.columns.name = "Column Name"
        guid = attributes['GUID']
        networks[guid] = {
            'edge_table': edge_table,
            'node_table': node_table,
            'name': attributes['Name'],
            'guid': guid }
    network_table = pd.DataFrame(graph_attributes)
    network_table.columns.name = "Column Name"
    return network_table, networks
    
def write_networks(folder, network_table, networks):
    """
    Writing networkTable, nodes and edges to Perseus readable format.
    
    :param folder: Path to output directory.
    :param network_table: Network table.
    :param networks: Dictionary with node and edge tables, indexed by network guid.
    """
    makedirs(folder, exist_ok=True) 
    network_table.to_perseus(path.join(folder, 'networks.txt'), main_columns=[])
    for guid, network in networks.items():
        network['node_table'].to_perseus(path.join(folder, '{}_nodes.txt'.format(guid)), main_columns=[])
        network['edge_table'].to_perseus(path.join(folder, '{}_edges.txt'.format(guid)), main_columns=[])
