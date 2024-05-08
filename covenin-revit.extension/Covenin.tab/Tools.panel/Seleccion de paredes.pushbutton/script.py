from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

walls = []

class SelectionFilter_Walls(ISelectionFilter):
    def AllowElement(self, element):
        if type(element) == Wall:
            return True

Wall_filter = SelectionFilter_Walls()
try:
    ref_picked_walls = uidoc.Selection.PickObjects(ObjectType.Element, Wall_filter)
    picked_walls = [doc.GetElement(ref) for ref in ref_picked_walls]
    for wall in picked_walls:
        width = wall.Width * 0.3048  # Convert to m
        length = wall.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsDouble() * 0.3048 # Convert to m
        area = wall.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsDouble() * 0.092903  # Convert to 

        walls.append({
            "Width": width,
            "Length": length,
            "Height": area / length,
            "Area": area,
            "Volume": area * width,
        })

    for wall in walls:
        print("Width: {}m".format(
            wall["Width"]))
        print("Length: {}m".format(wall["Length"]))
        print("Area: {}m2".format(wall["Area"]))
        print("Altura: {}m".format(wall["Height"]))
        print("Volumen: {}m3".format(wall["Volume"]))

except:
    SystemExit
