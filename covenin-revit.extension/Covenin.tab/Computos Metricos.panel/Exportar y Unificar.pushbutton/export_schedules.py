from pyrevit import DB, forms
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
import xlsxwriter


def export_selected_schedules(selected_schedules):
    path = forms.save_file(file_ext="xlsx")
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    schedules_data = []
    space_between_schedules = " "
    for scheds in selected_schedules:
        table_data = scheds.GetTableData()
        section_data = table_data.GetSectionData(DB.SectionType.Body)
        number_of_rows = section_data.NumberOfRows
        number_of_columns = section_data.NumberOfColumns

        for rows_number in range(number_of_rows):
            rows = []
            for columns_number in range(number_of_columns):
                cells_content = scheds.GetCellText(
                    DB.SectionType.Body, rows_number, columns_number
                )
                rows.append(cells_content)
            schedules_data.append(rows)
        schedules_data.append(space_between_schedules)

        for row_num, row_data in enumerate(schedules_data):
            for column_num, column_data in enumerate(row_data):
                worksheet.write(row_num, column_num, column_data)
    workbook.close()
