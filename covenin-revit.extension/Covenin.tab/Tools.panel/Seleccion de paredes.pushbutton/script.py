from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


class SelectionFilter_Walls(ISelectionFilter):
    def AllowElement(self,element):
        if type(element) == Wall:
            return True
        

Wall_filter = SelectionFilter_Walls()
ref_picked_walls = uidoc.Selection.PickObjects(ObjectType.Element,Wall_filter)
picked_walls  = [doc.GetElement(ref) for ref in ref_picked_walls]





