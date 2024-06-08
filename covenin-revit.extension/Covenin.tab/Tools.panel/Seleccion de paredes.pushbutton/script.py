from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from ppretty import ppretty

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

print(ppretty(__revit__))
print("********************")
print(ppretty(doc))
print("********************")
print(ppretty(uidoc))
