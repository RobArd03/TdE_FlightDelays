from logging import disable

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDaereoportoP = None
        self._choiceDDaereoportoP = None


    def handle_Analizza(self,e):
        self._view.txt_result.controls.clear()

        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico", color = "red"))
            self._view.update_page()
            return
        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un intero", color = "red"))
            self._view.update_page()
            return
        if cMin <= 0:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore maggiore di 0", color = "red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)

        allNodes = self._model.getAllNodes()
        self._fillDropDown(allNodes)

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

        self._view.update_page()

    def handle_Connessi(self,e):
        self._view.txt_result.controls.clear()
        if self._choiceDDaereoportoP is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare una voce dal menu", color = "red"))
            self._view.update_page()
            return
        viciniTuple = self._model.getSortedNeighbors(self._choiceDDaereoportoP)
        self._view.txt_result.controls.append(ft.Text(f"Diseguito i vicini di {self._choiceDDaereoportoP}"))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handle_CercaItinerario(self,e):
        self._view.txt_result.controls.clear()
        v0 = self._choiceDDaereoportoP
        v1 = self._choiceDDaereoportoD
        t = self._view._txtInTratteMax.value
        number = 0
        if t == "":
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico nelle tratte max", color = "red"))
            self._view.update_page()
            return
        try:
            number = int(t)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico nelle tratte massime", color = "red"))
            self._view.update_page()
            return

        path, scoretot = self._model.getCamminoOttimo(v0, v1, number)

        self._view.txt_result.controls.append(ft.Text(f"Cammino ottimo tra {v0} e {v1} ha peso = {scoretot} e d è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()

    def _fillDropDown(self,allNodes):
        for node in allNodes:
            self._view._ddAereoportoP.options.append(ft.dropdown.Option(
                data = node, key=node.IATA_CODE,
                on_click=self.pickDDpartenza ))
            self._view._ddAereoportoD.options.append(ft.dropdown.Option(
                data=node, key=node.IATA_CODE,
                on_click=self.pickDDdestinazione))

    def pickDDpartenza(self,e):
        self._choiceDDaereoportoP = e.control.data
        self._view._btnConnessi.disabled = False
        self._view.update_page()

    def pickDDdestinazione(self,e):
        self._choiceDDaereoportoD = e.control.data
        self._view._btnPercorso.disabled = False
        self._view._btnCerca.disabled = False
        self._view.update_page()

    def handle_Percorso(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceDDaereoportoP is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare una voce dal menu come partenza", color = "red"))
            self._view.update_page()
            return
        if self._choiceDDaereoportoD is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare una voce dal menu come destinazione", color = "red"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choiceDDaereoportoP, self._choiceDDaereoportoD)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Percorso tra i punti selezionati non esiste", color = "red"))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Percorso tra i punti selezionati esiste, di seguito i nodi del cammino"))
            for p in path:
                self._view.txt_result.controls.append( ft.Text(p) )
            self._view.update_page()

