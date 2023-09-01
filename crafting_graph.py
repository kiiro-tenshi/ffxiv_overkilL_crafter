# -*- coding: utf-8 -*-
'''
Created on Fri Sep  1 09:42:30 2023

@author: Kiiro Tenshi
'''

import networkx as nx
import matplotlib.pyplot as plt

def find_cheapest_way(materials_dict, target_item, verbose=False):
    G = nx.DiGraph()

    # Create the directed graph as before
    for material, ingredients in materials_dict.items():
        for ingredient, cost in ingredients.items():
            if material != target_item:
                G.add_edge(ingredient, material, cost=0)
            else:
                G.add_edge(ingredient, material, cost=cost)
            G.add_edge(ingredient, target_item, cost=cost)

    # Find the cheapest way to make the target item
    smallest_node = [node for node in G.nodes() if G.in_degree(node) == 0]
    groceries_list = {}
    total_cost = 0
    for node in smallest_node:
        cheapest_way = nx.shortest_path(G, source=node, target=target_item, weight='cost')
        cost = nx.shortest_path_length(G, source=node, target=target_item, weight='cost')
        #determine what to buy
        for i in range(len(cheapest_way)-1):
            edge_data = G.get_edge_data(cheapest_way[i], cheapest_way[i+1])
            if edge_data['cost'] != 0:
                groceries_list[cheapest_way[i]] = {'cost': cost, 'step': cheapest_way[i:]}
        total_cost += cost
    groceries_list['total_cost'] = total_cost
    
    # Visualization
    if verbose:
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_color='black')
        labels = nx.get_edge_attributes(G, 'cost')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

    return groceries_list

if __name__ == '__main__':
    materials_dict = {
        'Baked Eggplant': {'Dark Eggplant': 2, 'Garlean Cheese': 5, 'Frantoio Oil': 5,
                           'Blood Tomato': 2, 'Giant Popoto': 1, 'Earthbreak Aethersand': 10},
        'Garlean Cheese': {'Ovibos Milk': 10},
        'Frantoio Oil': {'Frantoio': 2}
    }
    target_item = 'Baked Eggplant'

    groceries_list = find_cheapest_way(materials_dict, target_item, verbose=True)
    print(groceries_list)