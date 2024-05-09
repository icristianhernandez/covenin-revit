from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import TaskDialog
import math

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_walls_data = []
volume_COVENIN_bricks = 0.00211  

def ft_to_m (feet_number):
    conversation_value = 0.3048
    return feet_number * conversation_value

def get_wall_layer_info(wall):
    """
    This function retrieves information about the name and width of each layer in a wall.

    Args:
        wall: A Revit Wall element.

    Returns:
        A dictionary where keys are material names and volume in feet.
    """
    # Check if the wall type has a compound structure (layered walls)
    compound_structure = wall.WallType.GetCompoundStructure()
    if not compound_structure:
        return {}  # Wall has no layers

    layer_info = {}
    for layer in compound_structure.GetLayers():
        material = doc.GetElement(layer.MaterialId)
        material_name = material.Name  # Assuming material has a name property
        layer_width = layer.Width  # Volume in cubic meters

        layer_info[material_name] = {
            "width": layer_width,
        }

    return layer_info


class SelectionFilter_Walls(ISelectionFilter):
    def AllowElement(self, element):
        if type(element) == Wall:
            return True


Wall_filter = SelectionFilter_Walls()
try:
    ref_picked_walls = uidoc.Selection.PickObjects(ObjectType.Element, Wall_filter)
    picked_walls = [doc.GetElement(ref) for ref in ref_picked_walls]
    bricks_layer_volume = 0

    for wall in picked_walls:
        extra_bricks_fix = 1.1

        width = ft_to_m( wall.Width )  
        length = (
            ft_to_m( wall.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsDouble() )
        )  
        area = (
            wall.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsDouble()
            * 0.092903
        )  
        name = wall.Name
        layer_info = get_wall_layer_info(wall)

        if layer_info:
            for material_name, data in layer_info.items():
                search_strings = [
                    "brick",
                    "Brick",
                    "BRICK",
                    "ladrillo",
                    "Ladrillo",
                    "LADRILLO",
                ]

                if any(string in material_name for string in search_strings):
                    bricks_layer_volume = data["width"] * area * 0.3048  # Convert to m3

        """
        The following data is calculated for each wall and added to the selected_walls_data list:

        - [width]: in meters.
        - [length]: in meters.
        - [height]: in meters.
        - [area]: in square meters.
        - [volume]: in cubic meters.
        - [name]: The name of the wall.
        - [bricks_layer_volume]: The volume of the bricks layer in cubic meters. If the wall has no bricks layer, this value is 0.
        - [necesary_bricks]: The number of bricks needed to build the wall. Assuming the standard volumen given by COVENIN in cubic meters and adding 10% extra bricks for precaution.
        """
        selected_walls_data.append(
            {
                "width": format(width, ".3f"),
                "length": format(length, ".3f"),
                "height": format(area / length, ".3f"),
                "area": format(area, ".3f"),
                "volume": format(area * width, ".3f"),
                "name": name,
                "bricks_layer_volume": (
                    format(bricks_layer_volume, ".3f") if bricks_layer_volume > 0 else 0
                ),
                "necesary_bricks": int(
                    
                    math.ceil(bricks_layer_volume / volume_COVENIN_bricks * extra_bricks_fix)
                ),
            }
        )
    report_main_text = ""
    bricks_total = 0
    for wall_data in selected_walls_data:
        bricks_total += int(wall_data["necesary_bricks"])

    if bricks_total == 0:
        report_main_text = "No se encontraron ladrillos en las paredes seleccionadas. Elija paredes soportadas por el programa (materiales soportados: ladrillo)."
    else:
        report_main_text = "Se necesitan " + str(bricks_total) + " ladrillos para construir las paredes seleccionadas."

    user_report = TaskDialog("COVENIN")
    user_report.TitleAutoPrefix = False
    user_report.MainInstruction = "COVENIN 2000 - Calculo de Ladrillos"
    user_report.MainContent = report_main_text 
    user_report.Show()

except:
    SystemExit
