from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

desired_schedule_parameters = [
    BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM,
    BuiltInParameter.HOST_AREA_COMPUTED,
    BuiltInParameter.HOST_VOLUME_COMPUTED,
    BuiltInParameter.CURVE_ELEM_LENGTH,
    BuiltInParameter.WALL_BASE_CONSTRAINT,
    BuiltInParameter.WALL_USER_HEIGHT_PARAM,
]

element_categorie = BuiltInCategory.OST_Walls


def create_schedule(doc, category, schedule_fields):
    """
    Create a schedule of all the elements of a given category with fields of the desired element parameters

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        category (BuiltInCategory): The category of the elements to be scheduled.
        schedule_fields (list): A list of BuiltInParameter values representing the element parameters to be included in the schedule.

    Returns:
        ViewSchedule: The created schedule with the desired fields.

    Examples:
        1. create_schedule(doc, BuiltInCategory.OST_Walls, [BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM, BuiltInParameter.WALL_BASE_CONSTRAINT])
           This example creates a schedule for walls with fields for element family and type parameter and wall base constraint parameter.

        2. create_schedule(doc, BuiltInCategory.OST_Doors, [BuiltInParameter.DOOR_NUMBER, BuiltInParameter.DOOR_WIDTH])
           This example creates a schedule for doors with fields for door number and door width parameters.

    Note:
        The schedule needs to be declared within a transaction in order to be properly created and modified.
    """
    all_id_of_category_elements = ElementId(category)

    schedule = ViewSchedule.CreateSchedule(doc, all_id_of_category_elements)
    schedule_def = schedule.Definition
    schedule_parameters_list = schedule_def.GetSchedulableFields()

    # add desired fields to the schedule
    for schedule_parameter_posibilities in schedule_parameters_list:
        for desired_parameter in schedule_fields:
            if schedule_parameter_posibilities.ParameterId == ElementId(desired_parameter):
                schedule_def.AddField(schedule_parameter_posibilities)

    return schedule


with Transaction(doc, "Schedule") as schedule_transaction:
    schedule_transaction.Start()

    schedule = create_schedule(doc, element_categorie, desired_schedule_parameters)

    schedule_transaction.Commit()

uidoc.ActiveView = schedule
