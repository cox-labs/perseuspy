import sys
from os import path
from unittest import TestCase, main
from io import StringIO

sys.path.insert(0, path.abspath(path.join(path.dirname( __file__ ), '..', 'io')))
from perseusNetwork import read_networks, _write_table

inFolder = path.join(path.dirname(__file__), "exampleNetworks", "networkFiles")

class Tests(TestCase):
	def test_reading(self):
		allDicts = read_networks(inFolder)
		self.assertTrue(not allDicts[0].empty and any(allDicts[1]) and any(allDicts[2]) and any(allDicts[3]) and any(allDicts[4]))
		nrNetw = len(allDicts[0].index)
		self.assertTrue(nrNetw == len(allDicts[1]) and nrNetw == len(allDicts[2]) and nrNetw == len(allDicts[3]) and nrNetw == len(allDicts[4]))
		
	def test_writing(self):
		allDicts = read_networks(inFolder)
		networkTable = StringIO()
		_write_table(networkTable, allDicts[0])
		nodes_list = []
		edges_list = []
		for key in allDicts[1]:
			nodes = StringIO()
			_write_table(nodes, allDicts[1][key])
			nodes_list.append(nodes)
		for key in allDicts[2]:
			edges = StringIO()
			_write_table(edges, allDicts[2][key])
			edges_list.append(edges)
		self.assertTrue(len(nodes_list) == len(edges_list) and len(edges_list) == allDicts[0].shape[0] and len(nodes_list) != 0)
		for tableio in nodes_list+edges_list:
			self.assertTrue(tableio.getvalue() != "")

if __name__ == '__main__':
    main()