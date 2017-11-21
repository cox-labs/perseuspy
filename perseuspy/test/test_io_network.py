import sys
from shutil import rmtree
from os import path, makedirs
from unittest import TestCase, main
from io import StringIO
from perseuspy import nx, pd, read_networks, write_networks

TEST_DIR = path.dirname(__file__)

class TestReadingAndWritingFromFolder(TestCase):
    def test_reading_single_network(self):
        networks_table, networks = read_networks(path.join(TEST_DIR, 'network_random'))
        self.assertEqual(3, networks_table.shape[0])
        self.assertEqual(3, len(networks))
        for guid, name in networks_table[['GUID', 'Name']].values:
            network = networks[guid]
            self.assertEqual(name, network['name'])
            node_table = network['node_table']
            self.assertEqual(100, node_table.shape[0])
            edge_table = network['edge_table']
            self.assertEqual(150, edge_table.shape[0])

    def test_writing(self):
        networks_table, networks = read_networks(path.join(TEST_DIR, 'network_random'))
        tmp_dir = path.join(TEST_DIR, 'tmp')
        makedirs(tmp_dir)
        write_networks(tmp_dir, networks_table, networks)
        _networks_table, _networks = read_networks(tmp_dir)
        self.assertTrue(networks_table.equals(_networks_table))
        guid = networks_table['GUID'][0]
        self.assertTrue(networks[guid]['node_table'].equals(_networks[guid]['node_table']))
        self.assertTrue(networks[guid]['edge_table'].equals(_networks[guid]['edge_table']))
        rmtree(tmp_dir)

class TestNetworkx(TestCase):
    def test_create_networkx_graph_duplicates(self):
        networks_table = pd.DataFrame({'GUID' : ['guid'], 'Name': ['net']})
        edge_table = pd.DataFrame({'Source': ['1', '1'], 'Target': ['2', '2']})
        node_table = pd.DataFrame({'Node': ['1', '1', '2']})
        import warnings
        with warnings.catch_warnings(record=True) as w:
            graphs = nx.from_perseus(networks_table, {'guid': {'name' : 'net', 'guid': 'guid', 'edge_table': edge_table, 'node_table': node_table}})
            self.assertEqual(2, graphs[0].number_of_nodes())
            self.assertEqual(1, graphs[0].number_of_edges())
            warning_messages = [str(x.message) for x in w if 'deprecated' not in str(x.message)]
            self.assertTrue('Duplicate edges' in warning_messages[0], warning_messages[0])
            self.assertTrue('Duplicate nodes' in warning_messages[1], warning_messages[1])

    def test_create_networkx_graph(self):
        networks_table, networks = read_networks(path.join(TEST_DIR, 'network_random'))
        graphs = nx.from_perseus(networks_table, networks)
        self.assertEqual(3, len(graphs))
        for i, G in enumerate(graphs):
            self.assertEqual(150, G.number_of_edges(), G.graph['Name'])
            self.assertEqual(100, G.number_of_nodes())

    def test_networkx_graph_roundtrip(self):
        networks_table, networks = read_networks(path.join(TEST_DIR, 'network_random'))
        graphs = nx.from_perseus(networks_table, networks)
        _networks_table, _networks = nx.to_perseus(graphs)
        self.assertTrue(networks_table.sort_index(axis=1).equals(_networks_table.sort_index(axis=1)))
        for guid in networks_table['GUID']:
            node_table = networks[guid]['node_table'].sort_values('Node').reset_index(drop=True)
            _node_table = _networks[guid]['node_table'].sort_values('Node').reset_index(drop=True)
            edge_table = networks[guid]['edge_table'].sort_values(['Source','Target']).reset_index(drop=True)
            _edge_table = _networks[guid]['edge_table'].sort_values(['Source', 'Target']).reset_index(drop=True)
            self.assertTrue(node_table.equals(_node_table))
            self.assertTrue(edge_table.equals(_edge_table))

    def test_empty_network_has_all_columns(self):
        G = nx.Graph()
        networks_table, networks = nx.to_perseus([G])
        for guid in networks_table['GUID']:
            node_table = networks[guid]['node_table']
            self.assertTrue('Node' in node_table.columns)
            edge_table = networks[guid]['edge_table']
            self.assertTrue('Source' in edge_table.columns)
            self.assertTrue('Target' in edge_table.columns)
        
if __name__ == '__main__':
    main()
