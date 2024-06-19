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

    schedule_fields = schedule_def.GetSchedulableFields()
    schedule_fields_names = []

    for schedulable_fields in schedule_fields:
        schedule_fields_names.append(schedulable_fields.GetName(doc))

    return schedule_fields_names


def debug_get_all_categories(doc):

    categories = doc.Settings.Categories
    categories_names = []

    for category in categories:
        categories_names.append(category.Name)

    return categories_names


def print_list_OfStrings(string_list):

    for string in string_list:
        print(string)


def get_ScheduleField_objets(doc, schedule):

    schedule_def = schedule.Definition
    schedule_fields_id = schedule_def.GetFieldOrder()
    schedule_fields = []

    for fieldId in schedule_fields_id:
        schedule_fields.append(schedule_def.GetField(fieldId))

    return schedule_fields


def add_schedule_sorting_field(doc, schedule, sort_settings):

    schedule_def = schedule.Definition
    current_fields = get_ScheduleField_objets(doc, schedule)
    # check if the field to be sorted is an current field comparing parameterID

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

    with Transaction(doc, "Schedule") as t:
        t.Start()

        category_id = ElementId(category)
        schedule = ViewSchedule.CreateSchedule(doc, category_id)
        schedule_def = schedule.Definition

        schedule = add_fields_to_schedule(doc, schedule, schedule_fields_parameter)
        if list_of_sort_settings:
            for sort_setting in list_of_sort_settings:
                schedule = add_schedule_sorting_field(doc, schedule, sort_setting)
        schedule_def.ShowGrandTotal = True
        schedule_def.ShowGrandTotalCount = True
        schedule_def.ShowGrandTotalTitle = True
        schedule_def.GrandTotalTitle = "Total: "

        # get schedule fields and set total to the last field
        # schedule_fields = get_ScheduleField_objets(doc, schedule)
        # schedule_fields[-1].CanTotal = True

        t.Commit()

    return schedule


def create_metric_calc_schedule(doc, element_category):

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
        {
            "field": metric_builtins[family_selected["metrics"]]["Value"],
            "sort_order": ScheduleSortOrder.Descending,
        },
    ]

    schedule = create_schedule(
        doc,
        element_categorie_revitID,
        desired_schedule_parameters,
        list_of_sort_settings,
    )

    return schedule
