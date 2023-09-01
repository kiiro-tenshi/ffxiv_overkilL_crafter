# -*- coding: utf-8 -*-
'''
Created on Fri Sep  1 09:42:30 2023

@author: Kiiro Tenshi
'''

import networkx as nx
import matplotlib.pyplot as plt

def create_recipe_graph(materials_dict, target_item, verbose=False):
    G = nx.DiGraph()

    for material, ingredients in materials_dict.items():
        for ingredient, cost in ingredients.items():
            if material != target_item:
                G.add_edge(ingredient, material, cost=0)
            else:
                G.add_edge(ingredient, material, cost=cost)
            G.add_edge(ingredient, target_item, cost=cost)

    if verbose:
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_color='black')
        labels = nx.get_edge_attributes(G, 'cost')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

    return G
        
if __name__ == '__main__':
    materials_dict = {
        'Baked Eggplant': {'Dark Eggplant': 2 ,'Garlean Cheese': 5, 'Frantoio Oil': 5, 
                           'Blood Tomato': 2, 'Giant Popoto': 1, 'Earthbreak Aethersand': 10},
        'Garlean Cheese': {'Ovibos Milk': 2},
        'Frantoio Oil': {'Frantoio': 2}
        }
    target_item = 'Baked Eggplant'
    G = create_recipe_graph(materials_dict, target_item, verbose=True)