# -*- coding: utf-8 -*-
from pyrevit import DB, forms
import xlsxwriter


def check_subtotal_unit(field):
    if field[0] == "Area" or field[0] == "Área":
        unit = "m²"
    elif field[0] == "Volume" or field[0] == "Volumen":
        unit = "m³"

    else:
        unit = ""
    return unit


def calculate_subtotal(column):
    new_column = []

    for item in column:
        if item:
            try:
                new_data = int(item.split()[0])
                new_column.append(new_data)
            except ValueError:
                pass

    sum_of_values = sum(new_column)
    subtotal = str(sum_of_values) + " "
    return subtotal


def export_selected_schedules(selected_schedules):
    try:
        path = forms.save_file(file_ext="xlsx")
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        sheet_name = "Tabla de Planificación Unificada"
        title_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 12,
                "align": "center",
                "bg_color": "#D3D3D3",
                "border": 1,
            }
        )
        borders_format = workbook.add_format({"border": 1, "align": "left"})
        worksheet.set_column("B:B", 32)
        schedules_data = []
        space_between_schedules = " "

        for scheds in selected_schedules:
            temporal_data = []
            subtotal_column = []
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

                temporal_data.append(rows)
                schedules_data.append(rows)

            for _, second_column in temporal_data:
                subtotal_column.append(second_column)

            subtotal = calculate_subtotal(subtotal_column)

            unit = check_subtotal_unit(subtotal_column)

            schedules_data.append(["SubTotal: ", subtotal + unit])
            schedules_data.append(space_between_schedules)

            del temporal_data[:]
            del subtotal_column[:]

        worksheet.merge_range("B1:C1", sheet_name, title_format)

        row = 1

        for schedule_rows in schedules_data:
            col = 1
            for cell_data in schedule_rows:
                if cell_data == " ":
                    worksheet.write(row, col, cell_data)
                else:
                    worksheet.write(row, col, cell_data, borders_format)
                    col += 1
            row += 1

        workbook.close()
    except:
        SystemExit
