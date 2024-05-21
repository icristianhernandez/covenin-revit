"""yo"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import WPFWindow
from pyrevit import script
from covenin_metric_calculation import create_metric_calc_schedule

xamlfile = script.get_bundle_file("interface.xaml")


class modalform(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.ShowDialog()

    def walls_push_button(self, sender, e):
        self.hide()

        def main():
            doc = __revit__.ActiveUIDocument.Document
            uidoc = __revit__.ActiveUIDocument
            # app = __revit__.Application

            selected_family_identifier = "Paredes"

            metric_schedule = create_metric_calc_schedule(
                doc, selected_family_identifier
            )

            uidoc.ActiveView = metric_schedule

        if __name__ == "__main__":
            main()
        self.Close()

    def floors_push_button(self, sender, e):
        self.hide()

        def main():
            doc = __revit__.ActiveUIDocument.Document
            uidoc = __revit__.ActiveUIDocument
            # app = __revit__.Application

            selected_family_identifier = "Suelos"

            metric_schedule = create_metric_calc_schedule(
                doc, selected_family_identifier
            )

            uidoc.ActiveView = metric_schedule

        if __name__ == "__main__":
            main()
        self.Close()

    def roofs_push_button(self, sender, e):
        self.hide()

        def main():
            doc = __revit__.ActiveUIDocument.Document
            uidoc = __revit__.ActiveUIDocument
            # app = __revit__.Application

            selected_family_identifier = "Techos"

            metric_schedule = create_metric_calc_schedule(
                doc, selected_family_identifier
            )

            uidoc.ActiveView = metric_schedule

        if __name__ == "__main__":
            main()
        self.Close()

    def cancel_button(self, sender, e):
        self.Close()


form = modalform("interface.xaml")
