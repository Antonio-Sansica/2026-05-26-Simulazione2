from database.DAO import DAO
from model.model import Model

mymodel = Model()

mymodel.build_graph(1.2, 2.7)
print(f"{mymodel.mappa_nodi}")
print(f"{mymodel.mappa_movies}")

#attori = DAO.getAll()

#print(len(attori))

#NODI
#n = mymodel.getNodi()
#print(f"il Grafo ha {len(n) } nodi")

#archi

#tutto dettagli
n, m = mymodel.get_dettagli_grafo()
print(f"Grafo creato: {n} nodi, {m} archi")