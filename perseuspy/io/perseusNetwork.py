import sys
import os
import networkx as nx
import collections
from perseuspy import pd # ugly -> change this to internal call
# Since Python 3 not needed anymore : 'from itertools import izip'

'''Note: The whole data structure for networks is represented via the list of the 5 following objects: 
		 networkTable, networkNodes = {GUID:nodeTable}, networkEdges = {GUID:edgeTable}, networkNameGUID = {Name:GUID}, networkGraph = {GUID:Graph}
		 
		 Important when changing graphs:
		 As 'writeNetworks(...)' currently  writes the networks from networkTable, networkNodes and networkEdges (not from networkGraph!),
		 networkGraph shall represent the same graphs as networkTable, networkNodes and networkEdges imply.
		 To keep this relation: When changing graph, simultaneously changing networkTables(network)
		 -> for example addEdge(), addNode(), removeEdge(), removeNode() necessary'''

def readNetworks( pathInFolder ):
	"Translating networks and corresponding node-/ and edgeTables to graphs"
	inFolder = pathInFolder
	networkTable = pd.read_perseus(inFolder+"\\networks.txt")
	networkNodes = collections.OrderedDict()
	networkEdges = collections.OrderedDict()
	networkNameGUID = collections.OrderedDict()
	networkGraph = collections.OrderedDict()

	for Name, GUID in zip(networkTable.Name, networkTable.GUID):
		G=nx.DiGraph() #directed graphs
		nodeTable = pd.read_perseus(inFolder+"\\"+GUID+"_nodes.txt")
		edgeTable = pd.read_perseus(inFolder+"\\"+GUID+"_edges.txt")
		networkNodes[GUID] = nodeTable
		networkEdges[GUID] = edgeTable
		networkNameGUID[Name] = GUID
		networkGraph[GUID] = G
		for Node in nodeTable.Node:
			G.add_node(Node)
		for Source, Target in zip(edgeTable.Source, edgeTable.Target):
			G.add_edge(Source, Target)
	allDicts = [networkTable, networkNodes, networkEdges, networkNameGUID, networkGraph]
	return allDicts
	

def writeNetworks( pathOutFolder , listAllDicts):
	"Writing networkTable, networkNodes and networkEdges in Perseus readable format"
	listAllDicts[0].to_perseus(pathOutFolder+"\\networks.txt")
	for key in listAllDicts[1]:
		listAllDicts[1][key].to_perseus(pathOutFolder+"\\"+key+"_nodes.txt")
	for key in listAllDicts[2]:
		listAllDicts[2][key].to_perseus(pathOutFolder+"\\"+key+"_edges.txt")		

		
def printNetworkNames( networkTable ):
	print ("\n All Networknames", end=": ")
	for Name, GUID in zip(networkTable.Name, networkTable.GUID):
		print (Name, end=", ")
	print ("\n")

	
def addNode( allDicts, nodeName , networkid):
   "This function adds a node to the Graph and corresponding nodeTable"
   '''todo: catch errors like: don't add existing node to networkNodes'''
   allDicts[4][networkid].add_node(nodeName)
   allDicts[1][networkid].loc[len(allDicts[1][networkid])] = nodeName
   return allDicts

