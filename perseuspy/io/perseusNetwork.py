from os import path
import networkx as nx
from collections import OrderedDict
from perseuspy import pd # ugly -> change this to internal call

def read_networks(pathInFolder):
	"""
	Translating networks and corresponding node-/ and edgeTables to graphs
	
	>>> allDicts = read_networks(pathinFolder)
	
	:param pathInFolder: Path to directory
	:returns: List of [networkTable, nodes, edges, nameGUID, graphs]
	"""
	networkTable = pd.read_perseus(path.join(pathInFolder, "networks.txt"))
	nodes = OrderedDict()
	edges = OrderedDict()
	nameGUID = OrderedDict()
	graphs = OrderedDict()
	for Name, GUID in zip(networkTable.Name, networkTable.GUID):
		G=nx.DiGraph()
		nodeTable = pd.read_perseus(path.join(pathInFolder, GUID + "_nodes.txt"))
		edgeTable = pd.read_perseus(path.join(pathInFolder, GUID + "_edges.txt"))
		nodes[GUID] = nodeTable
		edges[GUID] = edgeTable
		nameGUID[Name] = GUID
		graphs[GUID] = G
		for Node in nodeTable.Node:
			G.add_node(Node)
		for Source, Target in zip(edgeTable.Source, edgeTable.Target):
			G.add_edge(Source, Target)
	allDicts = [networkTable, nodes, edges, nameGUID, graphs]
	return allDicts
	
def write_networks(pathOutFolder, allDicts):
	"""
	Writing networkTable, nodes and edges to Perseus readable format
	
	Important when changing graphs:
	As 'writeNetworks(...)' currently  writes the networks from networkTable, nodes and edges (not from graphs!),
	graphs shall represent the same graphs as networkTable, nodes and edges imply.
	To keep this relation: When changing graph, simultaneously changing networkTables(network).
	-> For example add_edge(), add_node(), remove_edge(), remove_node() necessary.
		
	:param pathOutFolder: Path to directory
	:param allDicts: List of minimum networkTable, nodes and edges
	"""
	_write_table(path.join(pathOutFolder, "networks.txt"), allDicts[0])
	for key in allDicts[1]:
		_write_table(path.join(pathOutFolder, key + "_nodes.txt"), allDicts[1][key])
	for key in allDicts[2]:
		_write_table(path.join(pathOutFolder, key + "_edges.txt"), allDicts[2][key])

def _write_table(path_or_ioobject, table):
	"""
	Writing data frame to Perseus readable format. 
	
	:param path_or_ioobject: Path for creating file or StringIO object
	:param table: Pandas data frame
	"""
	table.to_perseus(path_or_ioobject)
			
def print_network_names(networkTable):
	"""
	Printing all network names.
	
	:param networkTable: Pandas data frame containing overview of the networks
	"""
	print ("\n All Networknames", end=": ")
	for Name, GUID in zip(networkTable.Name, networkTable.GUID):
		print (Name, end=", ")
	print ("\n")

def add_node(allDicts, nodeName , networkid):
   """
   This function adds a node to the Graph and corresponding nodeTable.
   Note: Adding a existing node, will lead to duplicate rows in nodeTable but no change in the corresponding graph!
   
   :param allDicts: List of [networkTable, nodes, edges, nameGUID, graphs]
   :param nodeName: Name of the node to be added
   :param networkid: GUID of the network the node will be added to
   :returns: List of [networkTable, nodes, edges, nameGUID, graphs]
   """
   allDicts[4][networkid].add_node(nodeName)
   allDicts[1][networkid].loc[len(allDicts[1][networkid])] = nodeName
   return allDicts

