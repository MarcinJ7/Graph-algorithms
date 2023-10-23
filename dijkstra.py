# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:59:10 2022

"""

# Dokonajmy testów szybkosci dzialania (grafy generujemy z wykorzystaniem pakietu networkx)

import networkx as nx
from algorithmx import jupyter_canvas
import random
from algorithmx.networkx import add_graph
import matplotlib.pyplot as plt

# Metoda tworzy losową liste sąsiedztwa
def generate_random_graph(n, p, plot=False):
    # Węzły -> n 
    # Prawdopodobieństwo utworzenia krawędzi
    #p = 0.8
    # Graf
    G = nx.gnp_random_graph(n, p)

    nx.set_edge_attributes(G, {e: {'weight': random.randint(1, 10)} for e in G.edges})
    
    G_data = nx.get_edge_attributes(G,'weight')
    
    # Utwórz listę sąsiedztwa
    graph_list = {}
    # Dla kazdej krawędzi wyszukujemy sąsiadów (gdzie możemy przejsc) i dodajemy do odpowiedniego klucza słownika wraz z wagą
    # Iterujemy przez słownik (węzeł start, węzeł końcowy), waga i dodajemy odpowidnio konstrukując listę sąsiedztwa
    for edges, weight in zip(G_data.keys(), G_data.values()):
        if edges[0] not in graph_list.keys():
            graph_list[edges[0]] = [(edges[1], weight)]          
        else:
            graph_list[edges[0]].append((edges[1], weight))
            
    # Jesli nie ma klucza zwiazanego z danym wierzcholkiem - umiesc tam pusta liste
    for i in range(n):
        if not i in graph_list.keys():
            graph_list[i] = []
    
    # Wyswietl graf
    if plot:
        plt.figure()    
        pos = nx.spring_layout(G)
        weight_labels = nx.get_edge_attributes(G,'weight')
        nx.draw(G,pos,font_color = 'white', node_shape = 's', with_labels = True,)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=weight_labels)
            
    return graph_list


numVertices = int(input('Podaj liczbe wierzcholkow grafu - zostanie wygenerowany losowo: '))

# Wygeneruj przykladowy graf skierowany
simple_graph = generate_random_graph(n  = numVertices, p = 0.8, plot=True)

# Przykładowy (mozna wykorzystać) - nieskierowany 
graph = {
    0: [(1, 1)],
    1: [(0, 1), (2, 2), (3, 3)],
    2: [(1, 2), (3, 1), (4, 5)],
    3: [(1, 3), (2, 1), (4, 1)],
    4: [(2, 5), (3, 1)]
}


import numpy as np

def dijkstra(simple_graph, start_vertice, end_vertice, verbose = True):
    
    # Graf w postaci listy sąsiedztwa - simple_graph
    # Wierzchołek startowy - start_vertice
    # Wierzchołek końcowy - end_vertice
    # Widocznosc verbose = True

    # Lista dystansów (równa liczbie wierzchołków)
    vertices_no = len(simple_graph)
    
    # Inicjalizacja listy dystansów nieskończonosciami 
    dist_list = [np.Inf for i in range(vertices_no)]
    # Oraz listy odwiedzonych wierzchołków
    visited_list = [False for i in range(vertices_no)]

    # Z wierzchołka startowego do startowego jest zerwoy dystans
    dist_list[start_vertice] = 0

    # Pętla po wszystkich wierzchołkach - wyznaczamy najkrótsze drogi do każdego z węzłów
    for v in range(vertices_no):
        # Wierzchołek "startowy" - jako -1 (warunek rozpoczęcia poszukiwań)
        ver = -1
        # Przeszukujemy wszystkie wierzchołki 
        for i in range(vertices_no):
            # Jesli analizowany wierzcholek nieodwiedzany i nie przetwarzany ("startowy") lub jego dystans jest mniejszy niz "startowy" dla tej iteracji
            if visited_list[i] == False and (ver == -1 or dist_list[i] < dist_list[ver]):
                # Wybierz ten wierzchołek jako kolejny do odwiedzenia 
                ver = i
                
        # Jeżeli nie możemy osiągnąć danego węzła po przeiterowaniu przez wszystkie - przerywamy pętlę 
        if dist_list[ver] == np.Inf:
            break
    
        # Wybrany wierzchołek oznaczamy jako odwiedzony
        visited_list[ver] = True
        
        
        # Porwównanie dystansów z węzła aktualnie "startowego" - wybór najkrótszego
        for next_node, distance in simple_graph[ver]:
            # Wybór najkrótszego dystansu
            if dist_list[ver] + distance < dist_list[next_node]:
                dist_list[next_node] = dist_list[ver] + distance 
        
    # Podsumowanie
    if verbose:
        print("Najkrótsza droga z węzła " + str(start_vertice) + " do węzła " + str(end_vertice) + " wynosi: " + str(dist_list[end_vertice]))
    
        # Wszystkie drogi:
        for idx, i in enumerate(dist_list):
            print("Wierzchołek " +str(start_vertice) + " do " + str(idx) +' odległosc: ' + str(i))
        
    return dist_list


start_ver = int(input('Podaj węzeł startowy: '))
end_ver = int(input('Podaj węzeł końcowy: '))


# Dijkstra - zwraca liste odległosci
distance_list = dijkstra(simple_graph = simple_graph, start_vertice = start_ver, end_vertice=end_ver)
