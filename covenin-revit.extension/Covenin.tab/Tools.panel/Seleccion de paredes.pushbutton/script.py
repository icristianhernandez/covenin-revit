from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def print_properties(self):
    for prop, value in vars(self).items():
        print(prop, ":", value) # or use format

doc.print_properties()
print("********************************")
uidoc.print_properties()
