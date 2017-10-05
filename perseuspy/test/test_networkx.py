import networkx as nx
from perseuspy.io.perseus.network import to_perseus

from unittest import TestCase, main
class TestConvertingBetweenNetworkxAndPerseus(TestCase):
    def test_random_graph(self):
        G = nx.random_graphs.barabasi_albert_graph(10, 3)
        f,t = G.edges()[0]
        G.edge[f][t]['Source'] = 'will be overwritten'
        G.edge[f][t]['Attribute'] = 'should show up'
        network_table, networks = to_perseus([G])
        self.assertTrue('Name' in network_table.columns)
        self.assertTrue('GUID' in network_table.columns)
        self.assertEqual(1, len(networks))
        network = list(networks.values())[0]
        self.assertEqual(G.name, network['name'])
        node_table = network['node_table']
        self.assertEqual(G.number_of_nodes(), node_table.shape[0])
        edge_table = network['edge_table']
        self.assertEqual(G.number_of_edges(), edge_table.shape[0])
        self.assertTrue(all(x in edge_table.columns for x in ['Source', 'Target']))
        self.assertEqual("0", edge_table['Source'][0])
        self.assertEqual('should show up', edge_table['Attribute'][0])

if __name__ == '__main__':
    main()
