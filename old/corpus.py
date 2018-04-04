from readwrite import xml_read_synsets
import networkx as ntwx

class RoWordNet(object):
    def __init__(self, file_path='resources//RoWn.xml'):
        self.graph = ntwx.DiGraph()
        self.xml_read(file_path)

    def xml_read(self, file_path):
        synsets = xml_read_synsets(file_path)

        for synset in synsets:
            self.graph.add_node(synset)
