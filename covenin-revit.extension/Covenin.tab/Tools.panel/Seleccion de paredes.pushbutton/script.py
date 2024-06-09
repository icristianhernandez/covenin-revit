from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
fec = FilteredElementCollector(doc)


all_walls_types = fec.OfClass(Wall).WhereElementIsElementType().ToElements()
all_walls = fec.OfClass(Wall).WhereElementIsNotElementType().ToElements()
print(all_walls)
print('----------------------------')
print(all_walls_types)
