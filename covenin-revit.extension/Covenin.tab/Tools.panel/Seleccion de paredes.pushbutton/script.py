from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
fec = FilteredElementCollector(doc)

t = Transaction(doc, 'Create family instance.')

t.Start()

all_families = fec.OfClass(FamilySymbol).ToElements()
print('----------------------------')
print(all_families)
 
t.Commit()
