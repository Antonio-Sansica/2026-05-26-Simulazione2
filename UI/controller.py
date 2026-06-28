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
        # 1. LETTURA INPUT E CONTROLLO ERRORI
        print("inizio grafo controller")
        valore_str = self._view._ddrating1.value
        valore2_str = self._view._ddrating2.value
        if valore_str is None or valore2_str is None:
            self._view.create_alert("Attenzione: Seleziona un range valido!")
            return

        try:
            parametro_utente = float(valore_str)
            parametro2_utente = float(valore2_str)
        except ValueError:
            self._view.create_alert("Attenzione: Seleziona un range valido!")
            return
        if parametro_utente > parametro2_utente:
            self._view.create_alert("Attenzione: Seleziona un range valido!")

        # 2. CHIAMATA AL MODEL
        self._model.build_graph(parametro_utente, parametro2_utente)

        # 3. PULIZIA SCHERMO E VERIFICA
        self._view.txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        # 4. STAMPA DELLE RISPOSTE STANDARD
        nodi, archi = self._model.get_dettagli_grafo()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

        # a) Stampa archi di peso maggiore
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="red"))
        top_archi = self._model.get_top_archi_peso(5)

        for u, v, dati in top_archi:
            # 🔴 RECUPERO I NOMI DALLA MAPPA USANDO GLI ID 'u' e 'v'
            nome_u = self._model.mappa_nodi[u].name
            nome_v = self._model.mappa_nodi[v].name
            self._view.txt_result.controls.append(ft.Text(f"{nome_u} -> {nome_v} ({dati['weight']})"))
        # b) Numero componenti connesse e componente maggiore
        num_comp, comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {num_comp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(comp_maggiore)} nodi):", color="red"))

        self._view.update_page()

    def handleCammino(self, e):
        pass