import heapq


class graphAlgo:

    def dijkstra(self, graph, start):
        """
        ITA: L'Algoritmo di Dijkstra è un algoritmo utilizzato per trovare il percorso più breve tra due nodi in un
        grafo con pesi sugli archi non negativi. L'algoritmo prende il nome dal suo inventore, l'informatico olandese
        Edsger Dijkstra.

            L'algoritmo di Dijkstra funziona attraverso l'iterazione sui nodi del grafo, assegnando loro un valore di
            distanza iniziale. Inizialmente, tutti i nodi vengono assegnati ad una distanza infinita, tranne il nodo
            di partenza, che viene assegnato ad una distanza di 0. L'algoritmo poi considera i nodi adiacenti al nodo
            di partenza e assegna loro una distanza in base al peso dell'arco che li collega. Questo processo viene
            ripetuto per tutti i nodi adiacenti fino a quando non viene trovato il percorso più breve dal nodo di
            partenza a tutti gli altri nodi del grafo.

            L'algoritmo di Dijkstra utilizza una coda di priorità per selezionare il nodo successivo da esaminare. A
            ogni iterazione, viene selezionato il nodo con la distanza minore dalla coda di priorità. Viene quindi
            esaminato il nodo selezionato e i suoi vicini, e viene aggiornata la distanza di ogni vicino se viene
            trovato un percorso più breve.

            L'Algoritmo di Dijkstra è utilizzato in molte applicazioni pratiche, come la pianificazione del percorso
            nelle reti stradali, la gestione del traffico aereo e la progettazione di reti di telecomunicazioni.

            La funzione dijkstra prende come parametri il grafo rappresentato da un dizionario di dizionari,
            dove ogni nodo è associato a un altro dizionario che contiene i suoi vicini e il peso degli archi che li
            collegano, e il nodo di partenza per il quale si vuole trovare il percorso più breve.

            La funzione inizializza un dizionario distances che assegna a ciascun nodo una distanza iniziale
            infinita, tranne il nodo di partenza che viene assegnato a una distanza di 0. Viene poi creato un heap (
            una coda di priorità) pq che contiene una tupla (distanza, nodo) inizializzata con la distanza del nodo
            di partenza e il nodo di partenza stesso. Viene anche inizializzato un insieme visited che tiene traccia
            dei nodi visitati.

            Il ciclo while continua fino a quando la coda di priorità pq non è vuota. Ad ogni iterazione,
            viene estratto il nodo con la distanza minore dalla coda di priorità. Viene quindi controllato se il nodo
            è già stato visitato. Se il nodo è già stato visitato, viene ignorato. Altrimenti, il nodo viene aggiunto
            all'insieme visited e si iterano i suoi vicini. Se la distanza dal nodo di partenza a un vicino è
            inferiore alla distanza attuale di quel vicino, la distanza del vicino viene aggiornata e la tupla (
            distanza, vicino) viene aggiunta alla coda di priorità pq.

            Infine, la funzione restituisce il dizionario distances, che contiene la distanza minima da ogni nodo al
            nodo di partenza.

            Ad esempio, supponiamo di avere il seguente grafo rappresentato dal dizionario di dizionari:
            graph = {
                        'A': {'B': 3, 'D': 1},
                        'B': {'A': 3, 'C': 2},
                        'C': {'B': 2, 'D': 4},
                        'D': {'A': 1, 'C': 4}
                    }

            Se vogliamo trovare il percorso più breve dal nodo 'A' a tutti gli altri nodi del grafo, possiamo
            chiamare la funzione dijkstra in questo modo:

            distances = dijkstra(graph, 'A')
            print(distances)

            L'output sarà:
            {'A': 0, 'B': 3, 'C': 5, 'D': 1}
            ovvero la distanza minima dal nodo 'A' è 0, dalla 'B' è 3, dalla 'C' è 5 e dalla 'D' è 1.
        """
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()

        while pq:
            (distance, node) = heapq.heappop(pq)

            if node in visited:
                continue

            visited.add(node)

            for neighbor, weight in graph[node].items():
                dist = distance + weight

                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    heapq.heappush(pq, (dist, neighbor))

        return distances

    def kruskal(self, graph):
        """
        ITA: L'Algoritmo di Kruskal è un algoritmo utilizzato per trovare il Minimum Spanning Tree (MST) di un grafo
        non orientato e pesato. Il MST è un sottoinsieme di archi che connette tutti i nodi del grafo con il peso
        totale minimo. L'algoritmo di Kruskal è basato sull'idea di ordinare gli archi del grafo in ordine crescente
        di peso e aggiungerli al MST se non formano un ciclo.

        La funzione kruskal prende come parametro un grafo rappresentato da un dizionario contenente un set di nodi e
        un set di archi con i rispettivi pesi. La funzione inizia creando un dizionario parent e un dizionario rank
        per tenere traccia del padre di ogni nodo e della sua altezza nell'albero. Viene poi definita la funzione
        make_set per inizializzare il set di ogni nodo, la funzione find per trovare il padre di un nodo e la
        funzione union per unire due set.

        Successivamente, viene creato un set vuoto minimum_spanning_tree che rappresenta l'MST. Vengono quindi
        estratti gli archi dal grafo e ordinati in ordine crescente di peso. Per ogni arco, si controlla se
        l'aggiunta dell'arco al MST forma un ciclo. Se l'arco non forma un ciclo, viene aggiunto al MST.

        Infine, la funzione restituisce il set minimum_spanning_tree, che contiene gli archi che formano l'MST.
        """
        parent = {}
        rank = {}

        def make_set(node):
            parent[node] = node
            rank[node] = 0

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)

            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root2] += 1

        for node in graph['vertices']:
            make_set(node)

        minimum_spanning_tree = set()
        edges = list(graph['edges'])
        edges.sort()

        for edge in edges:
            weight, node1, node2 = edge
            if find(node1) != find(node2):
                union(node1, node2)
                minimum_spanning_tree.add(edge)

        return minimum_spanning_tree