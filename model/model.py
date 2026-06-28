from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.grafo = nx.Graph()

    def get_ratings(self):
        return DAO.get_all_ratings()

    def popola_mappa(self, rate1, rate2):
        self.mappa_nodi.clear()  # 🚨 FONDAMENTALE: Pulisci la mappa ogni volta che l'utente clicca!
        lista_nodi = DAO.get_id_nodi_validi(rate1, rate2)

        for nodo in lista_nodi:
            # Filtro ninja suggerito dalla traccia: l'età deve avere senso logico!
            if nodo.eta >= 0:
                self.mappa_nodi[nodo.id] = nodo

    def build_graph(self, rate1, rate2):
        print("Inizio grafo model")
        self.grafo.clear()

        self.popola_mappa(rate1, rate2)
        self.grafo.add_nodes_from(self.mappa_nodi.keys())

        # Torniamo a chiamare il DAO SENZA parametri per il rating (avevi ragione tu!)
        archi_grezzi = DAO.get_archi_grafo_pesato()

        for id_1, id_2, idF, pesoParziale in archi_grezzi:

            if id_1 in self.mappa_nodi and id_2 in self.mappa_nodi:
                # 1. Pulisco il peso
                peso_pulito = 0
                if pesoParziale is not None:
                    try:
                        peso_str = pesoParziale.replace('$', '').replace(' ', '')
                        peso_pulito = int(peso_str)
                    except ValueError:
                        peso_pulito = 0

                # 2. Sommo o creo l'arco
                if self.grafo.has_edge(id_1, id_2):
                    self.grafo[id_1][id_2]['weight'] += peso_pulito
                else:
                    self.grafo.add_edge(id_1, id_2, weight=peso_pulito)

        # =========================================================
        # 3. IL TRUCCO FINALE: Rimuovo gli archi con incasso nullo
        # =========================================================
        archi_vuoti = []
        for u, v, dati in self.grafo.edges(data=True):
            if dati['weight'] == 0:
                archi_vuoti.append((u, v))

        self.grafo.remove_edges_from(archi_vuoti)  # Colpo di spugna!
    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_top_archi_peso(self, n):
        # 1. Estraggo tutti gli archi e li trasformo in lista
        lista_archi = list(self.grafo.edges(data=True))

        # 2. Li ordino in base al valore 'weight' dentro il dizionario 'data', al contrario (decrescente)
        lista_archi.sort(key=lambda edge: edge[2]['weight'], reverse=True)

        # 3. Restituisco i primi N elementi
        return lista_archi[:n]

    # =========================================================================
    # TRUCCO: COMPONENTE CONNESSA MAGGIORE (OPZIONE b e c)
    # =========================================================================
    def get_componente_connessa_maggiore(self):
        # 1. Quante sono in totale?
        num_componenti = nx.number_connected_components(self.grafo)

        # 2. Ottengo una lista di "set" (insiemi) contenenti i nodi di ciascuna componente connessa
        componenti = list(nx.connected_components(self.grafo))

        # 3. Trovo quella più grande usando len() come chiave per la ricerca del massimo
        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)


