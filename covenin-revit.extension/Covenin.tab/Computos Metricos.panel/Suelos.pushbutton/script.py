import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../utils/"))

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *
from covenin_metric_calculation import create_metric_calc_schedule


def main():
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    # app = __revit__.Application

    selected_family_identifier = "Suelos"

    metric_schedule = create_metric_calc_schedule(doc, selected_family_identifier)

    uidoc.ActiveView = metric_schedule


if __name__ == "__main__":
    main()
