"""yo"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import WPFWindow
from pyrevit import script
from covenin_metric_calculation import create_metric_calc_schedule

xamlfile = script.get_bundle_file("interface.xaml")

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


def main(x):
    selected_family_identifier = x

    metric_schedule = create_metric_calc_schedule(doc, selected_family_identifier)

    uidoc.ActiveView = metric_schedule


class modalform(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.ShowDialog()

    def walls_push_button(self, sender, e):
        self.hide()

        if __name__ == "__main__":
            main("Paredes")
        self.Close()

    def floors_push_button(self, sender, e):
        self.hide()

        if __name__ == "__main__":
            main("Suelos")
        self.Close()

    def roofs_push_button(self, sender, e):
        self.hide()

        if __name__ == "__main__":
            main("Techos")
        self.Close()

    def cancel_button(self, sender, e):
        self.Close()


form = modalform("interface.xaml")
