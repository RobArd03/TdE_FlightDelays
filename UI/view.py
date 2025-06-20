import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Tdp 2025 Flights Manager"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Welcome to the Tdp Flights Manager", color="green", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        # text field for the name


        self._txtInCMin = ft.TextField(label = "N companie minimo")
        self._btnAnalizza = ft.ElevatedButton(text="Analizza Aeroporti", on_click=self._controller.handle_Analizza)
        row1 = ft.Row([
            ft.Container(None, width=250),
            ft.Container(self._txtInCMin, width=250),
            ft.Container(self._btnAnalizza, width=250),
        ], ft.MainAxisAlignment.CENTER)


        self._ddAereoportoP = ft.Dropdown(label="Aeroporto di Partenza",)
        self._btnConnessi = ft.ElevatedButton(text="Aereoporto Connessi",
                                            on_click=self._controller.handle_Connessi,
                                              disabled=True)
        self._btnPercorso = ft.ElevatedButton(text="Trova Percorso",
                                              on_click=self._controller.handle_Percorso,
                                              disabled=True)
        row2 = ft.Row([
            ft.Container(self._ddAereoportoP, width=250),
            ft.Container(self._btnConnessi, width=250),
            ft.Container(self._btnPercorso, width=250),
        ], ft.MainAxisAlignment.CENTER)

        self._ddAereoportoD = ft.Dropdown(label="Aeroporto di Destinazione",)
        self._txtInTratteMax = ft.TextField(label = "N Tratte Max")
        self._btnCerca = ft.ElevatedButton(text="Cerca Itinerario",
                                           on_click=self._controller.handle_CercaItinerario,
                                           disabled=True)
        row3 = ft.Row([
            ft.Container(self._ddAereoportoD, width=250),
            ft.Container(self._txtInTratteMax, width=250),
            ft.Container(self._btnCerca, width=250),
        ], ft.MainAxisAlignment.CENTER)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        row4 = ft.Row([self.txt_result])

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)
        self._page.controls.append(row4)






        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
