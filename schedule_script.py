
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.ApplicationServices import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


def ScheduleFields(sfs):
    structure_parameters = [BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM, BuiltInParameter.HOST_AREA_COMPUTED, BuiltInParameter.HOST_VOLUME_COMPUTED,
                            BuiltInParameter.CURVE_ELEM_LENGTH, BuiltInParameter.WALL_BASE_CONSTRAINT, BuiltInParameter.WALL_USER_HEIGHT_PARAM]
    for sp in structure_parameters:
        if ElementId(sp) == sfs.ParameterId:
            return True
    return False


def create_schedule(doc):

    id = ElementId(BuiltInCategory.OST_Walls)
    schedule = ViewSchedule.CreateSchedule(doc, id)
    schedule_def = schedule.Definition
    schedulable_fields = schedule_def.GetSchedulableFields()
    for sf in schedulable_fields:
        if ScheduleFields(sf):
            schedule_def.AddField(sf)

    return schedule


t = Transaction(doc, "Schedule")
t.Start()
schedule = create_schedule(doc)
t.Commit()
uidoc.ActiveView = schedule
