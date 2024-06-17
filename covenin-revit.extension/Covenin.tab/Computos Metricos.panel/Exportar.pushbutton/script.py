# import pyrevit libraries
from pyrevit import revit, DB, forms, script
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
import xlsxwriter


# import libraries

selected_schedules = forms.select_schedules()
schedules = []
if selected_schedules:
    for sched in selected_schedules:
        schedules.append(sched)

    # destination = forms.pick_folder()
    path = forms.save_file(file_ext="xlsx")
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    schedules_data = []
    space_between_schedules = " "

    for sched in schedules:
        table_data = sched.GetTableData()
        section_data = table_data.GetSectionData(DB.SectionType.Body)
        number_of_rows = section_data.NumberOfRows
        number_of_columns = section_data.NumberOfColumns

        for rows_number in range(number_of_rows):
            rows = []
            for columns_number in range(number_of_columns):
                content = sched.GetCellText(
                    DB.SectionType.Body, rows_number, columns_number
                )
                rows.append(content)
            schedules_data.append(rows)
        schedules_data.append(space_between_schedules)

        for row_num, row_data in enumerate(schedules_data):
            for column_num, colum_data in enumerate(row_data):
                worksheet.write(row_num, column_num, colum_data)

    workbook.close()
