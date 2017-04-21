import os
from os import path
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'io')))
from perseusNetwork import readNetworks, writeNetworks

DIR = path.dirname(__file__)

class Tests(unittest.TestCase):
	"""Tests for perseusNetwork.py"""

	def test_reading(self):
		allDicts = readNetworks(os.path.join(DIR, "exampleNetworks", "networkFiles"))
		self.assertTrue(not allDicts[0].empty  and any(allDicts[1]) and any(allDicts[2]) and any(allDicts[3]) and any(allDicts[4])) # check on empty dictionaries
		nrNetw = len(allDicts[0].index)
		self.assertTrue(nrNetw == len(allDicts[1]) and nrNetw == len(allDicts[2]) and nrNetw == len(allDicts[3]) and nrNetw == len(allDicts[1])) # check size of created dictionaries
		
	def test_writing(self):
		outDir = os.path.join(DIR, "exampleNetworks", "outDirectory")
		dictlist = readNetworks(os.path.join(DIR, "exampleNetworks", "networkFiles"))
		writeNetworks(outDir, dictlist)
		self.assertTrue(len(dictlist[4])*2+1+1 == len([name for name in os.listdir(outDir) if os.path.isfile(os.path.join(outDir, name))])) # check number of created files, +1(networks.txt), +1(dummy file)

if __name__ == '__main__':
    unittest.main()
