from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *


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

        2.
            with Transaction(doc, "Schedule") as schedule_transaction:
                schedule_transaction.Start()
                schedule = create_schedule(doc, BuiltInCategory.OST_Walls, [BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM])
                schedule_transaction.Commit()
            __revit__.ActiveUIDocument.ActiveView = schedule

    Note:
        The schedule needs to be declared within a transaction in order to be properly instantiated in the Revit document.
        After, the schedule need to be added to the active view in order to be displayed: uidoc.ActiveView = schedule
    """

    all_id_of_category_elements = ElementId(category)

    schedule = ViewSchedule.CreateSchedule(doc, all_id_of_category_elements)
    schedule_def = schedule.Definition
    schedule_parameters_list = schedule_def.GetSchedulableFields()

    # add only the desired fields to the schedule
    for schedule_parameter_posibilities in schedule_parameters_list:
        for desired_parameter in schedule_fields:
            if schedule_parameter_posibilities.ParameterId == ElementId(
                desired_parameter
            ):
                schedule_def.AddField(schedule_parameter_posibilities)

    return schedule


def create_metric_calc_schedule(doc, element_category):
    """
    Create a schedule of all the elements of a given category with fields of the
    metric calculation based on the COVENIN standards.

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        element_category (BuiltInCategory): The category of the elements to be scheduled.

    Returns:
        ViewSchedule: The created schedule with the desired fields.

    Examples:
        1. create_metric_calc_schedule(doc, "Paredes")
           This example creates a schedule for walls with fields for the metric calculation based on the COVENIN standards.

    Currently supported element categories:
        "Paredes"
        "Techos"
        "Suelos"
    """
    covenin_metrics_of_elements = {
        "Paredes": {
            "revit_category": BuiltInCategory.OST_Walls,
            "metrics": BuiltInParameter.HOST_AREA_COMPUTED,
        },
        "Techos": {
            "revit_category": BuiltInCategory.OST_Ceilings,
            "metrics": BuiltInParameter.HOST_AREA_COMPUTED,
        },
        "Suelos": {
            "revit_category": BuiltInCategory.OST_Floors,
            "metrics": BuiltInParameter.HOST_AREA_COMPUTED,
        },
    }

    family_selected = covenin_metrics_of_elements[element_category]

    element_categorie = family_selected["revit_category"]
    desired_schedule_parameters = [
        BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM,
        family_selected["metrics"],
    ]

    with Transaction(doc, "Schedule") as schedule_transaction:
        schedule_transaction.Start()
        schedule = create_schedule(doc, element_categorie, desired_schedule_parameters)
        schedule_transaction.Commit()

    return schedule


def main():
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    app = __revit__.Application

    family_selected_identifier = "Paredes"

    metric_schedule = create_metric_calc_schedule(doc, family_selected_identifier)

    uidoc.ActiveView = metric_schedule


if __name__ == "__main__":
    main()
