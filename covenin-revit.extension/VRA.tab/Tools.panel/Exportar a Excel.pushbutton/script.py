from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import WPFWindow
from pyrevit import script
from export_schedules import export_selected_schedules
from covenin_schedules_creation import create_metric_calc_schedule

xamlfile = script.get_bundle_file("export_interface.xaml")

DOC = __revit__.ActiveUIDocument.Document
UIDOC = __revit__.ActiveUIDocument


def delete_schedule_sheet_instance(DOC, schedules_to_delete):
    with Transaction(DOC, "Delete Schedules") as t:
        t.Start()
        DOC.Delete(schedules_to_delete.Id)
        t.Commit()


def create_and_export_covenin_calc_schedules(selected_family_identifier):
    selected_schedules = []
    for categories in selected_family_identifier:
        selected_schedules.append(create_metric_calc_schedule(DOC, categories))

    export_selected_schedules(selected_schedules)
    for schedules_to_delete in selected_schedules:
        delete_schedule_sheet_instance(DOC, schedules_to_delete)


class modalform(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.available_families = {
            self.bordes_losa: "Bordes de Losa",
            self.cubiertas: "Cubiertas",
            self.disp_ilum: "Dispositivos de Iluminacion",
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
        self.categories = []
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
                self.categories.append(identifier)

        create_and_export_covenin_calc_schedules(self.categories)
        self.Close()

    def cancel_button(self, sender, e):
        self.Close()


if __name__ == "__main__":
    form = modalform("export_interface.xaml")
