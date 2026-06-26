import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        a = self._view.ddyear.value
        state_id = self._view.ddstate.value
        if a is None or state_id is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno e uno stato per procedere"))
            self._view.update_page()
            return
        try:
            anno = int(a)
        except:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("anno non numerico"))
            self._view.update_page()

        self._model.buildGraph(anno, state_id)
        n,a = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"grafo creato correttamente con {n} nodi e {a} archi"))
        num, largest = self._model.getInfoConnessa()
        self._view.txt_result1.controls.append(ft.Text(f"Numero componenti connesse : {num}"))
        for l in largest:
            self._view.txt_result1.controls.append(ft.Text(f"{l.id}--{l.city}--{l.datetime}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDYears(self):
        years = self._model.getAllYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))
        self._view.ddyear.on_change = self.fillDDStatesByYear #NO PARAMETRI
        self._view.update_page()


    def fillDDStatesByYear(self, e=None):   #DEVO METTERLO PERCHE VIENE SCATENATO DA ON CHANGE
        a = self._view.ddyear.value
        if a is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno per procedere"))
            self._view.update_page()
            return
        try:
          anno = int(a)
        except:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("anno non numerico"))
            self._view.update_page()

        stati = self._model.getStatesByYear(anno)
        for s in stati:
            self._view.ddstate.options.append(ft.dropdown.Option(key=s.id, text = s.name, data = s))
        self._view.update_page()
