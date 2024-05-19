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
        doc (Document): Revit Document
        category (BuiltInCategory): Category of the elements to be scheduled
        schedule_fields (list): List of BuiltInParameter to be included in the schedule

    Returns:
        ViewSchedule: Schedule with the desired fields
    """
    elements_id_of_category = ElementId(category)

    schedule = ViewSchedule.CreateSchedule(doc, elements_id_of_category)
    schedule_def = schedule.Definition
    schedule_parameters_list = schedule_def.GetSchedulableFields()

    # add only the desired fields to the schedule
    for schedule_parameter in schedule_parameters_list:
        for desired_parameter in schedule_fields:
            if schedule_parameter.ParameterId == ElementId(desired_parameter):
                schedule_def.AddField(schedule_parameter)

    return schedule


with Transaction(doc, "Schedule") as schedule_transaction:
    schedule_transaction.Start()

    schedule = create_schedule(doc, element_categorie, desired_schedule_parameters)

    schedule_transaction.Commit()

uidoc.ActiveView = schedule
