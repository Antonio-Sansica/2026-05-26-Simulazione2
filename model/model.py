import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.mappa_incassi = {}
        self.grafo = nx.Graph()
    def get_ratings(self):
        return DAO.getAllRatings()

    def popola_mappa_nodi(self, rate1, rate2):
        self.mappa_nodi.clear()
        lista_nodi = DAO.getAllNodi(rate1, rate2)
        lista_movies = DAO.getAllMovies(rate1, rate2)
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.id] = nodo
            for movie, attore in lista_movies:
                if attore == nodo.id:
                    self.mappa_nodi[nodo.id].movies.add(movie)

    def popola_mappa_incassi(self, rate1, rate2):
        self.mappa_incassi.clear()
        lista_nodi = DAO.getAllIncassi(rate1, rate2)
        for movie, incasso in lista_nodi:
            self.mappa_incassi[movie] = incasso

    def build_graph(self, rate1, rate2):
        self.grafo.clear()
        self.popola_mappa_incassi(rate1, rate2)
        self.popola_mappa_nodi(rate1, rate2)

        self.grafo.add_nodes_from(self.mappa_nodi.values())

        lista_nodi = list(self.grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i+1, len(lista_nodi)):
                a1 = lista_nodi[i]
                a2 = lista_nodi[j]
                movies = a1.movies & a2.movies
                nmovies = len(movies)

                if nmovies > 0:
                    peso = 0
                    for movie in movies:
                        incasso = self.mappa_incassi[movie].replace('$','').replace(' ','')
                        peso += int(incasso)
                    self.grafo.add_edge(a1, a2, weight=peso)

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

        for nodo_partenza in self.grafo.nodes():
            parziale = [nodo_partenza]
            self._ricorsione_cammino_vincolo_nodi(parziale)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_cammino_vincolo_nodi(self, parziale):
        # 1. VALUTAZIONE: Stiamo cercando il percorso più LUNGO
        if len(parziale) > self._punteggio_ottimo:
            self._punteggio_ottimo = len(parziale)
            self._soluzione_ottima = list(parziale)

        # 2. ESPLORAZIONE
        ultimo_nodo = parziale[-1]

        # Uso .neighbors() per i grafi non orientati (come richiesto in questo esame)
        for vicino in self.grafo.neighbors(ultimo_nodo):

            # VINCOLO A (La traccia chiede "Cammino Semplice"): Non ripassare sui nodi
            if vicino not in parziale:

                # VINCOLO B (Speciale): "Età strettamente decrescente"
                # Confronto l'attributo .eta (che devi aver messo nel DTO) del vicino
                # con l'attributo .eta del nodo in cui mi trovo ora.

                # Sostituisci '.eta' con l'attributo reale del tuo DTO all'esame!
                if vicino.eta < ultimo_nodo.eta:
                    # 3. AZIONE E BACKTRACKING
                    parziale.append(vicino)
                    self._ricorsione_cammino_vincolo_nodi(parziale)
                    parziale.pop()



