from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.mappa_movies = {}
        self.grafo = nx.Graph()

    def getRatings(self):
        return DAO.getAllRatings()

    def popola_mappe(self, rate1, rate2):
        self.mappa_nodi.clear()
        self.mappa_movies.clear()
        lista_nodi = DAO.getAllNodi(rate1, rate2)
        lista_movies = DAO.getAllMovies(rate1, rate2)
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.id] = nodo
            for artist, movie, incasso  in lista_movies:
                if artist in self.mappa_nodi:
                    self.mappa_nodi[artist].movies.add(movie)
                self.mappa_movies[movie] = incasso

    def build_graph(self, rate1, rate2):
        self.grafo.clear()
        self.popola_mappe(rate1, rate2)

        self.grafo.add_nodes_from(self.mappa_nodi.values())

        lista_nodi = list(self.grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i+1, len(lista_nodi)):
                a1 = lista_nodi[i]
                a2 = lista_nodi[j]

                if a1.id in self.mappa_nodi and a2.id in self.mappa_nodi:

                    movies = a1.movies & a2.movies

                    if len(movies) > 0:
                        peso = 0
                        for movie in movies:
                            if self.mappa_movies[movie] is not None:
                                peso += int(self.mappa_movies[movie].replace('$','').replace(' ',''))
                            else:
                                peso += 0
                        self.grafo.add_edge(a1, a2, weight=peso)


    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_top_archi_peso(self, n):
        lista_archi = list(self.grafo.edges(data=True))

        lista_archi.sort(key=lambda edge: edge[2]['weight'], reverse=True)

        # 3. Restituisco i primi N elementi
        return lista_archi[:n]

    def get_numero_componenti_connesse(self):
        if self.grafo.number_of_nodes() == 0: return 0
        return nx.number_connected_components(self.grafo)

    def get_componente_connessa_maggiore(self):
        num_componenti = nx.number_connected_components(self.grafo)

        componenti = list(nx.connected_components(self.grafo))

        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)

