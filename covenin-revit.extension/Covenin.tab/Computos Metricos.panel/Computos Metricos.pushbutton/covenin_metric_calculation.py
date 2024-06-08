from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *


def add_fields_to_schedule(doc, schedule, list_of_fields_object):
    schedule_def = schedule.Definition
    schedule_fields = schedule_def.GetSchedulableFields()

    for desired_field in list_of_fields_object:
        # print(desired_field["Type"])
        # print(desired_field["Value"].GetType())
        # print("----")
        for possible_field in schedule_fields:
            if desired_field["Type"] == "BuiltIn":
                if possible_field.ParameterId == ElementId(desired_field["Value"]):
                    schedule_def.AddField(possible_field)
            if desired_field["Type"] == "ScheduleFieldType":
                if possible_field.FieldType == desired_field["Value"]:
                    schedule_def.AddField(possible_field)

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


def print_list_OfStrings(string_list):
    """
    Print a list of strings in a readable format

    Args:
        string_list (list of strings): The list of strings to be printed.
    """
    for string in string_list:
        print(string)


def get_ScheduleField_objets(doc, schedule):
    """
    Return a list with the current fields of a schedule in the same order they
    have in the schedule.

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        schedule (ViewSchedule): The schedule to which the fields will be added.

    Returns:
        schedule_fields (list of SchedulableField): A list of the current fields of the schedule.
    """
    schedule_def = schedule.Definition
    schedule_fields_id = schedule_def.GetFieldOrder()
    schedule_fields = []

    for fieldId in schedule_fields_id:
        schedule_fields.append(schedule_def.GetField(fieldId))

    return schedule_fields


def add_schedule_sorting_field(doc, schedule, sort_settings):
    """
    Add an sorting field with settings to a schedule

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        schedule (ViewSchedule): The schedule to which the sorting field will be added.
        sort_settings (dict of ScheduleSortGroupField settings): A dictionary with the settings of the sorting field.

    Returns:
        ViewSchedule: The schedule with the added sorting field.

    Examples:
        1. add_schedule_sorting_field(doc, schedule, {"field": BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM, "order": ScheduleSortOrder.Ascending})
              This example adds a sorting field for element family and type parameter in ascending order to the schedule.

    Notes:
        1) If the field to be sorted not exist in the schedule, don't add the sorting field.
        2) The sort_settings dictionary can have the following keys and value:
            - "field": The class of the field to be sorted.
            - "show_blank_line": A boolean value to show a blank line between the groups.
            - "show_footer": A boolean value to show the footer.
            - "show_footer_count": A boolean value to show the count in the footer.
            - "show_footer_title": A boolean value to show the title in the footer.
            - "show_header": A boolean value to show the header.
            - "sort_order": The order of the sorting field. It can be ScheduleSortOrder.Ascending or ScheduleSortOrder.Descending.
        3) Fields that cannot be sorted: "Count"
    """
    schedule_def = schedule.Definition
    current_fields = get_ScheduleField_objets(doc, schedule)
    # check if the field to be sorted is an current field comparing parameterID
    sort_settings["field"] = BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM

    sort_by_ScheduleFieldId = 0
    can_be_sorted_by_that_parameter = False
    sort_group = ScheduleSortGroupField()
    exception_fields = [ScheduleFieldType.Count]

    # Exit when the field to be sorted is an exception field
    if sort_settings["field"] in exception_fields:
        return schedule

    # Exit when the field to be sorted does not exist in the schedule
    for field in current_fields:
        if field.ParameterId == ElementId(sort_settings["field"]):
            sort_by_ScheduleFieldId = field.FieldId
            can_be_sorted_by_that_parameter = True
            break
    if not can_be_sorted_by_that_parameter:
        return schedule

    # Exit when no field is provided
    if "field" not in sort_settings:
        return schedule

    # Exit when the field provided is blank
    if sort_settings["field"] == "":
        return schedule

    sort_group.FieldId = sort_by_ScheduleFieldId
    if "show_blank_line" in sort_settings:
        sort_group.ShowBlankLine = sort_settings["show_blank_line"]
    if "show_footer" in sort_settings:
        sort_group.ShowFooter = sort_settings["show_footer"]
    if "show_footer_count" in sort_settings:
        sort_group.ShowFooterCount = sort_settings["show_footer_count"]
    if "show_footer_title" in sort_settings:
        sort_group.ShowFooterTitle = sort_settings["show_footer_title"]
    if "show_header" in sort_settings:
        sort_group.ShowHeader = sort_settings["show_header"]
    if "sort_order" in sort_settings:
        sort_group.SortOrder = sort_settings["sort_order"]

    schedule_def.AddSortGroupField(sort_group)

    return schedule


def create_schedule(
    doc, category, schedule_fields_parameter, list_of_sort_settings=None
):
    """
    Create a schedule of all the elements of a given category with fields of the desired element parameters

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        category (BuiltInCategory): The category of the elements to be scheduled.
        schedule_fields (list of strings): List of SchedulableField names to be included in the schedule.
        list_of_sort_settings(list of dicts): List of dictionaries with the settings of the sorting fields.

    Returns:
        ViewSchedule: The created schedule with the desired fields.

    Examples:
        1. create_schedule(doc, BuiltInCategory.OST_Walls, ["Family and Type", "Base Constraint"])
           This example creates a schedule for walls with fields for element family and type parameter and wall base constraint parameter.

    Note:
        1) If wanted modify the schedule outside the function, that modification must be done inside a transaction.
        2) After, if wanna asign a tab to the schedule: uidoc.ActiveView = schedule
        3) For the list_of_sort_settings, see the documentation of add_schedule_sorting_field function.
    """
    with Transaction(doc, "Schedule") as t:
        t.Start()

        category_id = ElementId(category)
        schedule = ViewSchedule.CreateSchedule(doc, category_id)
        schedule_def = schedule.Definition

        schedule = add_fields_to_schedule(doc, schedule, schedule_fields_parameter)
        if list_of_sort_settings:
            for sort_setting in list_of_sort_settings:
                schedule = add_schedule_sorting_field(doc, schedule, sort_setting)

        t.Commit()

    return schedule


def create_metric_calc_schedule(doc, element_category):
    """
    Create a schedule of all the elements of a given category with fields of the
    metric calculation based on the COVENIN standards.

    Args:
        doc (Document): The Revit document in which the schedule will be created.
        element_category (string): The category name of the elements to be scheduled. Check supported names in notes

    Returns:
        ViewSchedule: The created schedule with the desired fields.

    Examples:
        1. create_metric_calc_schedule(doc, "Paredes")
           This example creates a schedule for walls with fields for the metric calculation based on the COVENIN standards.

    Currently supported element categories:
        "Paredes"
        "Techos"
        "Suelos"
        "Columnas"
        "Puertas"
        "Bordes de Losa"
        "Mobiliario"
        "Sistemas de Mobiliario"
        "Iluminacion"
        "Dispositivos de Iluminacion"
        "Plantas"
        "Cubiertas"
        "Escaleras"
        "Estructuras Temporales"
        "Ventanas"
        "Muros Cortina"

    Notes:
        Needed be assigned to the active view in order to be displayed as tab: uidoc.ActiveView = schedule
    """
    covenin_metrics_of_elements = {
        "Paredes": {"revit_category": BuiltInCategory.OST_Walls, "metrics": "Area"},
        "Techos": {"revit_category": BuiltInCategory.OST_Ceilings, "metrics": "Area"},
        "Suelos": {"revit_category": BuiltInCategory.OST_Floors, "metrics": "Area"},
        "Puertas": {"revit_category": BuiltInCategory.OST_Doors, "metrics": "Count"},
        "Bordes de Losa": {
            "revit_category": BuiltInCategory.OST_EdgeSlab,
            "metrics": "Length",
        },
        "Mobiliario": {
            "revit_category": BuiltInCategory.OST_Furniture,
            "metrics": "Count",
        },
        "Sistemas de Mobiliario": {
            "revit_category": BuiltInCategory.OST_FurnitureSystems,
            "metrics": "Count",
        },
        "Iluminacion": {
            "revit_category": BuiltInCategory.OST_LightingFixtures,
            "metrics": "Count",
        },
        "Dispositivos de Iluminacion": {
            "revit_category": BuiltInCategory.OST_LightingDevices,
            "metrics": "Count",
        },
        "Plantas": {"revit_category": BuiltInCategory.OST_Planting, "metrics": "Count"},
        "Cubiertas": {"revit_category": BuiltInCategory.OST_Roofs, "metrics": "Area"},
        "Estructuras Temporales": {
            "revit_category": BuiltInCategory.OST_TemporaryStructure,
            "metrics": "Volume",
        },
        "Ventanas": {"revit_category": BuiltInCategory.OST_Windows, "metrics": "Count"},
        "Muros Cortina": {
            "revit_category": BuiltInCategory.OST_CurtainWallPanels,
            "metrics": "Area",
        },
    }
    metric_builtins = {
        "Length": {"Type": "BuiltIn", "Value": BuiltInParameter.CURVE_ELEM_LENGTH},
        "Area": {"Type": "BuiltIn", "Value": BuiltInParameter.HOST_AREA_COMPUTED},
        "Volume": {"Type": "BuiltIn", "Value": BuiltInParameter.HOST_VOLUME_COMPUTED},
        "Count": {"Type": "ScheduleFieldType", "Value": ScheduleFieldType.Count},
    }

    family_selected = covenin_metrics_of_elements[element_category]

    element_categorie_revitID = family_selected["revit_category"]
    desired_schedule_parameters = [
        {"Type": "BuiltIn", "Value": BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM},
        metric_builtins[family_selected["metrics"]],
    ]
    list_of_sort_settings = [
        {
            "field": BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM,
            "show_blank_line": True,
            "sort_order": ScheduleSortOrder.Ascending,
            "show_footer": True,
            "show_footer_count": True,
            "show_header": True,
        },
        # {
        #     "field": family_selected["metrics"],
        #     "sort_order": ScheduleSortOrder.Descending,
        # },
    ]

    schedule = create_schedule(
        doc,
        element_categorie_revitID,
        desired_schedule_parameters,
        list_of_sort_settings,
    )

    return schedule
