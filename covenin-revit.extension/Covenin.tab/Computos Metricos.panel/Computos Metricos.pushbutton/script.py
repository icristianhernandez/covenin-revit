from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import WPFWindow
from pyrevit import script
from covenin_metric_calculation import create_metric_calc_schedule

xamlfile = script.get_bundle_file("interface.xaml")

DOC = __revit__.ActiveUIDocument.Document
UIDOC = __revit__.ActiveUIDocument


def create_and_show_covenin_calc_schedules(selected_family_identifier):
    UIDOC.ActiveView = create_metric_calc_schedule(DOC, selected_family_identifier)


class modalform(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.available_families = {
            self.bordes_losa: "Bordes de Losa",
            self.columnas: "Columnas",
            self.cubiertas: "Cubiertas",
            self.disp_ilum: "Dispositivos de Iluminacion",
            self.escaleras: "Escaleras",
            self.estruct_temp: "Estructuras Temporales",
            self.ilum: "Iluminacion",
            self.mobiliario: "Mobiliario",
            self.muro_cortina: "Muros Cortina",
            self.planta: "Plantas",
            self.pared: "Paredes",
            self.puerta: "Puertas",
            self.sistem_mob: "Sistemas de Mobiliario",
            self.suelo: "Suelos",
            self.techo: "Techos",
            self.ventana: "Ventanas",
        }
        self.ShowDialog()

    def select_all_options(self, sender, e):
        for selected_options, _ in self.available_families.items():
            selected_options.IsEnabled = True
            selected_options.IsChecked = True

    def uncheck_all_options(self, sender, e):
        for unselected_options, _ in self.available_families.items():
            unselected_options.IsChecked = False

    def accept_button(self, sender, e):
        self.hide()
        for selected_options, identifier in self.available_families.items():
            if selected_options.IsChecked:
                user_selection_identifier = identifier
                create_and_show_covenin_calc_schedules(user_selection_identifier)
        self.Close()

    def cancel_button(self, sender, e):
        self.Close()


if __name__ == "__main__":
    form = modalform("interface.xaml")
