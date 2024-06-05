from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *

def add_fields_to_schedule(doc, schedule, list_fields_name):
    """
    Add fields to a schedule

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        schedule (ViewSchedule): The schedule to which the fields will be added.
        list_fields_name (list of strings): A list of BuiltInParameter values representing the element parameters to be included in the schedule.

    Returns:
        ViewSchedule: The schedule with the added fields.

    Examples:
        1. add_fields_to_schedule(doc, schedule, ["Family and Type", "Base Constraint"])
              This example adds fields for element family and type parameter and wall base constraint parameter to the schedule.
    """
    schedule_def = schedule.Definition
    schedule_fields = schedule_def.GetSchedulableFields()

    for desired_fields in list_fields_name:
        for schedulable_fields in schedule_fields:
            if schedulable_fields.GetName(doc) == desired_fields:
                schedule_def.AddField(schedulable_fields)

    return schedule

def debug_get_schedulable_fields_names(doc, schedule_def):
    """
    Return a list with the names of the schedulable fields of a schedule

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        schedule (ViewSchedule): The schedule to which the fields will be added.

    Returns:
        schedule_fields_names (list of strings): A list of the names of the schedulable fields of the schedule.
    """
    schedule_fields = schedule_def.GetSchedulableFields()
    schedule_fields_names = []

    for schedulable_fields in schedule_fields:
        schedule_fields_names.append(schedulable_fields.GetName(doc))

    return schedule_fields_names

def debug_get_all_categories(doc):
    """
    Return a list with the names of all the categories in the Revit document

    Args:
        doc (Document): The Revit document in which the schedule will be created.

    Returns:
        categories_names (list of strings): A list of the names of all the categories in the Revit document.
    """
    categories = doc.Settings.Categories
    categories_names = []

    for category in categories:
        categories_names.append(category.Name)

    return categories_names

def print_string_list(string_list):
    """
    Print a list of strings in a readable format

    Args:
        string_list (list of strings): The list of strings to be printed.
    """
    for string in string_list:
        print(string)

def create_schedule(doc, category, schedule_show_fields):
    """
    Create a schedule of all the elements of a given category with fields of the desired element parameters

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        category (BuiltInCategory): The category of the elements to be scheduled.
        schedule_fields (list of strings): List of SchedulableField names to be included in the schedule.

    Returns:
        ViewSchedule: The created schedule with the desired fields.

    Examples:
        1. create_schedule(doc, BuiltInCategory.OST_Walls, ["Family and Type", "Base Constraint"])  
           This example creates a schedule for walls with fields for element family and type parameter and wall base constraint parameter.

    Note:
        The schedule needs to be declared within a transaction in order to be properly instantiated in the Revit document.
        After, the schedule need to be added to the active view in order to be displayed: uidoc.ActiveView = schedule
    """

    all_id_of_category_elements = ElementId(category)

    schedule = ViewSchedule.CreateSchedule(doc, all_id_of_category_elements)
    schedule_def = schedule.Definition

    # print_string_list(debug_get_all_categories(doc))
    # print_string_list(debug_get_schedulable_fields_names(doc, schedule_def)))
    schedule = add_fields_to_schedule(doc, schedule, schedule_show_fields)

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

    Notes: 
        Needed be assigned to the active view in order to be displayed as tab: uidoc.ActiveView = schedule
    """
    covenin_metrics_of_elements = {
        "Paredes": {
            "revit_category": BuiltInCategory.OST_Walls,
            "metrics": "Area"
        },
        "Techos": {
            "revit_category": BuiltInCategory.OST_Ceilings,
            "metrics": "Area"
        },
        "Suelos": {
            "revit_category": BuiltInCategory.OST_Floors,
            "metrics": "Area"
        },
    }

    family_selected = covenin_metrics_of_elements[element_category]

    element_categorie = family_selected["revit_category"]
    desired_schedule_parameters = [
        "Family and Type",
        family_selected["metrics"],
    ]

    with Transaction(doc, "Schedule") as schedule_transaction:
        schedule_transaction.Start()
        schedule = create_schedule(doc, element_categorie, desired_schedule_parameters)
        schedule_transaction.Commit()

    return schedule
