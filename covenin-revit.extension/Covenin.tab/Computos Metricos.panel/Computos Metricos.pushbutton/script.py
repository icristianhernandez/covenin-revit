from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import WPFWindow
from pyrevit import script
from covenin_metric_calculation import create_metric_calc_schedule

xamlfile = script.get_bundle_file("interface.xaml")

DOC = __revit__.ActiveUIDocument.Document
UIDOC = __revit__.ActiveUIDocument


def create_and_show_metric_schedule(selected_family_identifier):
    UIDOC.ActiveView = create_metric_calc_schedule(DOC, selected_family_identifier)


class modalform(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.ShowDialog()

    def walls_push_button(self, sender, e):
        self.hide()
        user_selection_identifier = "Paredes"
        create_and_show_metric_schedule(user_selection_identifier)
        self.Close()

    def floors_push_button(self, sender, e):
        self.hide()
        user_selection_identifier = "Suelos"
        create_and_show_metric_schedule(user_selection_identifier)
        self.Close()

    def roofs_push_button(self, sender, e):
        self.hide()
        user_selection_identifier = "Techos"
        create_and_show_metric_schedule(user_selection_identifier)
        self.Close()

    def cancel_button(self, sender, e):
        self.Close()


if __name__ == "__main__":
    form = modalform("interface.xaml")
