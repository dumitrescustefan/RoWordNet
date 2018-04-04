from components import Relation, Literal, Synset
from corpus import RoWordNet
import networkx as nx

if __name__ == '__main__':
    g = nx.DiGraph()

    syn1 = Synset('a', definition='adadad')
    syn2 = Synset('b')
    syn3 = Synset('c')
    syn4 = Synset('d')

    g.add_edge(syn1.id, syn2.id, label='hyper')
    g.add_edge(syn2.id, syn3.id, label='hypo')
    g.add_edge(syn1.id, syn4.id)
    g.add_edge(syn2.id, syn4.id)

    g.node['a']['def'] = 'adadada'
    g.node['b']['def'] = 'adada'
    g.node['c']['def'] = 'dadwad'

    g.node['a']['pos'] = '+'
    g.node['b']['pos'] = '-'
    g.node['c']['pos'] = '='

    print(nx.shortest_path(g,'a','d'))

    print(g.node['a'])
    print(g.node['b'])
    print(g.node['c'])






