import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.mappa_incassi = {}
        self.popola_mappa_incassi()
        self.grafo = nx.Graph()

    def get_ratings(self):
        return DAO.getAllRatings()

    def popola_mappa_nodi(self, r1, r2):
        self.mappa_nodi.clear()
        lista_nodi = DAO.getAllNodi(r1, r2)
        lista_movies = DAO.getAllMovies(r1, r2)
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.id] = nodo
            for attore, movie in lista_movies:
                if attore == nodo.id:
                    nodo.movies.add(movie)

    def popola_mappa_incassi(self):
        self.mappa_incassi.clear()
        lista_incassi = DAO.getAllIncassi()
        for movie, incasso in lista_incassi:
            self.mappa_incassi[movie] = int(incasso.replace('$', '').replace(' ',''))

    def build_graph(self, r1, r2):
        self.grafo.clear()
        self.popola_mappa_nodi(r1, r2)
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        lista_nodi = list(self.grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i + 1, len(lista_nodi)):
                n1 = lista_nodi[i]
                n2 = lista_nodi[j]

                movies_in_comune = n1.movies & n2.movies

                if len(movies_in_comune) > 0:
                    peso = 0
                    for movie in movies_in_comune:
                        peso += self.mappa_incassi[movie]

                    self.grafo.add_edge(n1, n2, weight=peso)

    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_top_archi_peso(self, n):
        lista_archi = list(self.grafo.edges(data=True))

        lista_archi.sort(key=lambda edge: edge[2]['weight'], reverse=True)

        return lista_archi[:n]

    def get_componente_connessa_maggiore(self):
        num_componenti = nx.number_connected_components(self.grafo)

        componenti = list(nx.connected_components(self.grafo))

        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)




    def calcola_percorso_lungo_con_vincolo_nodi(self):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0

        lista_nodi = list(self.grafo.nodes())

        for nodo in lista_nodi:
            parziale = [nodo]

            self._ricorsione_cammino_vincolo_nodi(parziale)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_cammino_vincolo_nodi(self, parziale):
        if len(parziale) > self._punteggio_ottimo:
            self._punteggio_ottimo = len(parziale)
            self._soluzione_ottima = list(parziale)

        ultimo_nodo = parziale[-1]

        for vicino in self.grafo.neighbors(ultimo_nodo):

            if vicino not in parziale:

                if vicino.date_of_birth > ultimo_nodo.date_of_birth:
                    parziale.append(vicino)
                    self._ricorsione_cammino_vincolo_nodi(parziale)
                    parziale.pop()

