import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        self._view._ddrating1.options.clear()
        self._view._ddrating2.options.clear()
        dati = self._model.get_ratings()
        for dato in dati:
            self._view._ddrating1.options.append(ft.dropdown.Option(str(dato)))
            self._view._ddrating2.options.append(ft.dropdown.Option(str(dato)))

    def handleCreaGrafo(self, e):
        valore_str1 = self._view._ddrating1.value
        valore_str2 = self._view._ddrating2.value

        if valore_str1 is None or valore_str2 is None:
            self._view.create_alert("Attenzione: Seleziona un range valido!")
            return

        try:
            parametro_utente1 = float(valore_str1)
            parametro_utente2 = float(valore_str2)
        except ValueError:
            self._view.create_alert("Attenzione: Seleziona un range valido!")
            return

        if parametro_utente1 > parametro_utente2:
            self._view.create_alert("Attenzione: Seleziona un range valido!")
            return


        self._model.build_graph(parametro_utente1, parametro_utente2)

        self._view.txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        nodi, archi = self._model.get_dettagli_grafo()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

        self._view.txt_result.controls.append(ft.Text("5 Archi di peso maggiore:", color="red"))
        top_archi = self._model.get_top_archi_peso(5)
        for u, v, dati in top_archi:
            self._view.txt_result.controls.append(ft.Text(f"{u.name} -> {v.name} ({dati['weight']})"))

        num_comp, comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {num_comp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(comp_maggiore)} nodi):", color="red"))

        for nodo in comp_maggiore:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.name}"))
        self._view.update_page()

    def handleCammino(self, e):
        self._view.txt_result.controls.clear()

        percorso_nodi, lunghezza = self._model.calcola_percorso_lungo_con_vincolo_nodi()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato percorso lungo {lunghezza} attori:", color="red", weight="bold")
        )
        for nodo in percorso_nodi:
            self._view.txt_result.controls.append(ft.Text(f"- {nodo.name} (DOB: {nodo.date_of_birth})"))

        self._view.update_page()