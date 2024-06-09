from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
import pprint

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

pprint.pprint(__revit__)
print("********************")
pprint.pprint(doc)
print("********************")
pprint.pprint(uidoc)
