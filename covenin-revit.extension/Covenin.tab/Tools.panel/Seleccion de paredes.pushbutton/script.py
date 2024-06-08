from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# create a new wall family type
wallType = WallType.Create(doc, "MyWallType")

print("Wall type created: ", wallType.Name)
