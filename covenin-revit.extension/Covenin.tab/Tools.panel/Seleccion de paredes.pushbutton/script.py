from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
fec = FilteredElementCollector(doc)

all_families = fec.OfClass(FamilySymbol).ToElements()
print('----------------------------')

for item in all_families:
    print(item.Name)

