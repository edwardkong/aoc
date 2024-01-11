import networkx as nx
import math

class Wires:
    def __init__(self, nodes):
        self.network = self.parse_edges_into_network(nodes)

    def parse_edges_into_network(self, nodes):
        network = nx.Graph()
        for n in nodes:
            node, edges = n.split(':')
            for edge in edges.strip().split():
                network.add_edge(node, edge)
        return network
    
    def cut_min(self):
        network = self.network
        cut_wires = nx.minimum_edge_cut(network)
        assert len(cut_wires) == 3, f'Expected 3 wires, got {len(cut_wires)}'

        network.remove_edges_from(cut_wires)
        return math.prod(len(sub) for sub in nx.connected_components(network))

def main_part_one():
    with open('day25/input.txt', 'r') as file:
        lines = file.read().splitlines()
    w = Wires(lines)
    return w.cut_min()

if __name__ == '__main__':
    print(main_part_one())