from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
import pprint

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
fec = FilteredElementCollector(doc)


all_walls = fec.OfClass(Wall).ToElements()
print(all_walls)
print('----------------------------')
print(fec.OfClass(Wall)) 
