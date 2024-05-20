from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *
from covenin_adaptation import create_metric_calc_schedule 

def main():
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    # app = __revit__.Application

    selected_family_identifier = "Paredes"

    metric_schedule = create_metric_calc_schedule(doc, selected_family_identifier)

    uidoc.ActiveView = metric_schedule


if __name__ == "__main__":
    main()
