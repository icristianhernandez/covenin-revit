from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

walls = []

def get_wall_length(document, wall):

  # Check if the element is a valid wall
  if not isinstance(wall, Wall):
    return None

  # Get the wall's location curve
  location_curve = wall.Location

  # Access the curve object from the location curve
  curve = location_curve.Curve

  # Get the start and end points of the curve
  start_point = curve.GetEndPoint(0)
  end_point = curve.GetEndPoint(1)

  # Calculate the distance between the points using XYZ.DistanceTo
  length = start_point.DistanceTo(end_point)

  return length

class SelectionFilter_Walls(ISelectionFilter):
    def AllowElement(self, element):
        if type(element) == Wall:
            return True


Wall_filter = SelectionFilter_Walls()
try:
    ref_picked_walls = uidoc.Selection.PickObjects(ObjectType.Element, Wall_filter)
    picked_walls = [doc.GetElement(ref) for ref in ref_picked_walls]
    for wall in picked_walls:
        walls.append({
            "Width": wall.Width,
            "Length": get_wall_length(doc, wall)
        })

    for wall in walls:
        print("Width: {} Length: {}".format(wall["Width"], wall["Length"]))
except:
    SystemExit
