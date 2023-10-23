# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:22:58 2022

@author: Marcin
"""

# Cześć, mam do przygotowania projekt polegający na porównaniu efektywności przechodzenia 
# po grafach, za pomocą DFS, BFS oraz sortowania za pomocą Algorytmu Kahna. Niezależne 
# jest czy działamy na macierzy sąsiedztwa, czy jakiejś innej, mają być takie same 
# informacje i podsumowanie, która z reprezentacji jest lepsza. Program napisany w Pythonie. 


# Macierz sąsiedztwa
# Na początku reprezentacja grafu - macierz sąsiedztwa lub lista sąsiedztwa (N x N) - N - liczba węzłów w grafie
# Wiersze reprezentują węzły, a kolumny potencjalne "dzieci" tych węzłów. 

# Lista sąsiedztwa
# To zbiór kilku listy. Każda lista repreznetuje węzeł w grafie i przechowuje sąsiadów/dzieci tego węzła.


# Implementacja algorytmów przeszukowania

def dfs(graph_list, start_node, path=[]):
    # Zaczynamy od start_node - dodajemy go do sciezki
    path.append(start_node)
    # Przechodzimy przez sasiadow dodajac kolejnych do sciezki rekurencyjne
    for node in graph_list[start_node]:
        # Jezeli sasiad nie jest jeszcze w sciezce - wyszukaj jego sasiadow
        if node not in path:
            path = dfs(graph_list, node, path)
    return path


# RUN : Example: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

graph_list = {
    0: [1,2],
    1: [2],
    2: [0, 3],
    3: [3]
    }

dfs(graph_list, start_node=2, path=[])


def bfs(graph_list, start_node, path=[]):
    # Zaczynamy od start_node - dodajemy go do sciezki
    path.append(start_node)
    # Dodajemy węzeł do kolejki
    queue = [start_node]
    
    # Przechodzimy przez kolejkę
    while len(queue) > 0:
        # Zdejmujemy wierzchołek z kolejki ...
        node_off = queue.pop(0)
        # ...i przechodizmy przez jego sasiadów 
        for node in graph_list[node_off]:
            # Oczywiscie sasiadow nieodwiedznaych
            if node not in path:
                # Dodaj węzeł do odwiedzonych (sciezka)
                path.append(node)
                # Oraz do kolejki 
                queue.append(node)
                
    return path
    
# RUN : Example: https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/breadth-first-search-bfs-algorithm/

graph_list2 = {
    0: [1,2],
    1: [2,4],
    2: [3],
    3: [],
    4: []
    }

bfs(graph_list2, 0, path=[])


# Dokonajmy testów szybkosci dzialania (grafy generujemy z wykorzystaniem pakietu networkx)

from networkx.generators.random_graphs import erdos_renyi_graph
import networkx

# Metoda tworzy losową liste sąsiedztwa
def generate_random_graph(n, plot=False):
    # Węzły
    # n = 6
    # Prawdopodobieństwo utworzenia krawędzi
    p = 0.8
    # Graf
    g = erdos_renyi_graph(n, p)
    
    # Wypisz węzły
    #print(g.nodes)
    # Wypisz kwaędzie
    #print(g.edges)
    
    # Utwórz listę sąsiedztwa
    graph_list = {}
    # Dla kazdej krawędzi wyszukujemy sąsiadów (gdzie możemy przejsc) i dodajemy do odpowiedniego klucza słownika 
    for edge in list(g.edges):
        if edge[0] not in graph_list.keys():
            graph_list[edge[0]] = [edge[1]]
        else:
            graph_list[edge[0]].append(edge[1])
            
    # Jesli nie ma klucza zwiazanego z danym wierzcholkiem - umiesc tam pusta liste
    for i in range(n):
        if not i in graph_list.keys():
            graph_list[i] = []
    
    # Wyswietl graf
    if plot:
        networkx.draw(g, with_labels=True)
    
    return graph_list

# Wygeneruj przykladowy graf
simple_graph = generate_random_graph(10, plot=True)

print(bfs(simple_graph, 0, path=[]))
print(dfs(simple_graph, 0, path=[]))


# Pomiar czasu dla różnych wielkosci grafu (10..100) -> (start..stop)
import time

bfs_time = []
dfs_time = []
start = 10
stop = 301

for i in range(start, stop):
    # Generuj graf
    simple_graph = generate_random_graph(i)
    # Start pomiaru czasu
    tic = time.perf_counter()
    # BFS
    bfs(simple_graph, 0, path=[])
    # Koniec pomiaru czasu
    toc = time.perf_counter()
    # Dodaj czas do tablicy
    bfs_time.append(toc-tic)

     # Start pomiaru czasu
    tic = time.perf_counter()
    # DFS
    dfs(simple_graph, 0, path=[])
    # Koniec pomiaru czasu
    toc = time.perf_counter()
    # Dodaj czas do tablicy
    dfs_time.append(toc-tic)

# Porównanie na wykresie
import matplotlib.pyplot as plt

plt.plot(list(range(start, stop)), bfs_time)
plt.plot(list(range(start, stop)), dfs_time)
plt.legend(['BFS', 'DFS'])
plt.title('Porownanie czasow BFS i DFS')
plt.xlabel('Węzły grafu')
plt.ylabel('Czas w [s]')

# print(np.mean(bfs_time))
# print(np.mean(dfs_time))

# Sortowanie Kahna: http://knma.wikidot.com/algorytmy-grafowe:sortowanie-topologiczne-kahn
# http://www.cs.put.poznan.pl/mszachniuk/mszachniuk_files/lab_aisd/Szachniuk-ASD-t3.pdf


def kahnSort(graph_list):
    # Utworzmy liste ze stopniami wejsciowymi
    list_degree_in = (len(graph_list))*[0]
    
    # Iterujemy i jeżeli węzeł wchodzi do innego wezla - inkrementujemy
    for key in graph_list.keys():
        for item in graph_list[key]:
            list_degree_in[item] += 1
    
    # Tworzymy listę wierzcholkow ze stopniem wejsciowym rownym 0
    queue = []
    
    for node_number in range(len(list_degree_in)):
        if list_degree_in[node_number] == 0:
            queue.append(node_number)
    
    # Counter - do zliczania odwiedzanych wierzcholkow
    counter = 0
    # Posortowane wierzcholki
    sorted_nodes = []
    
    # Przechodzimy przez wszystkie wezly z kolejki
    while len(queue) > 0:
        # Pobieramy węzeł z kolejki
        node_off = queue.pop(0)
        # Dodajemy do listy posortowanych wierzcholkow
        sorted_nodes.append(node_off)
    
        # Odejmujemy kolejno stopie wiezchołków sąsiadujących
        for node in graph_list[node_off]:
            list_degree_in[node] -= 1
            # Sprawdzamy, czy jakis stopien nie jest juz rowny zero
            if list_degree_in[node] == 0:
                # Jezeli tak - dodajemy do kolejki
                queue.append(node)
                
        counter+=1
    
    if counter!= len(graph_list):
        print('Graf zawiera cykle - sortowanie niemozliwe')
    else:
        print('Posortowane wierzcholki:')
        print(sorted_nodes)


graph_list3 = {
    0: [3, 5],
    1: [3, 4],
    2: [4, 7],
    3: [5, 6],
    4: [6, 7],
    5: [],
    6: [],
    7: []
    }

# Sortowanie
kahnSort(graph_list3)

kahnTime = []
start = 10
stop = 301

# Pomiar czasu 
for i in range(start, stop):
    # Generuj graf
    simple_graph = generate_random_graph(i)
    # Start pomiaru czasu
    tic = time.perf_counter()
    # Sortowanie kahn
    kahnSort(simple_graph)
    # Koniec pomiaru czasu
    toc = time.perf_counter()
    # Dodaj czas do tablicy
    kahnTime.append(toc-tic)

# Porównanie na wykresie
import matplotlib.pyplot as plt

plt.plot(list(range(start, stop)), kahnTime)
plt.title('Sortowanie algorytmem Kahna')
plt.xlabel('Węzły grafu')
plt.ylabel('Czas w [s]')
