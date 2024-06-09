from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
import pprint

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

pprint.pp(__revit__)
print("********************")
pprint.pp(doc)
print("********************")
pprint.pp(uidoc)
