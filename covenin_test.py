"""
From a .py file, get the line number of the file where the elements of a list are defined.
The files need to be named as: covenin_data_scrapped.py
The list needs to be named as: covenin_elements_data
covenin_elements_data need to be a list of dictionaries

Each dictionary needs to have the following keys: 
    - nombre
    - codigo_covenin
    - unidad_de_medida
    - categoria_revit

The names can't repeat.

The covenin codes can't repeat.

The values of the key "unidad_de_medida" need to be one of the following:
    - m
    - m2
    - m3
    - cantidad

The values of the key "categoria_revit" need to be one of the following:
    (left for now)
    - test
    - example
"""

import ast
import os
from covenin_data_scrapped import covenin_elements_data


def get_line_number_of_list_elements(file_path, list_name):
    """
    Get the line number of the file where the elements of a list are defined.

    Args:
        file_path (str): The path of the .py file.
        list_name (str): The name of the list.

    Returns:
        List with the line files of each element of the target list (list of int): The line number of the file where the elements of the list are defined.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
        tree = ast.parse(file_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if node.targets[0].id == list_name:
                    return [node.lineno + 1 for node in node.value.elts]


def is_last_character(string_to_check, character):
    """
    Check if the last character of a string is equal to a given character.

    Args:
        string_to_check (str): The string to check.
        character (str): The character to check.

    Returns:
        True if the last character of the string is equal to the character, False otherwise (bool).
    """
    return string_to_check[-1] == character


def remove_last_characters(string_to_affect, characters_to_remove=1):
    """
    Remove the last characters of a string.

    Args:
        string_to_affect (str): The string to affect.
        characters_to_remove (int): The number of characters to remove.

    Returns:
        The string without the last characters (str).
    """
    return string_to_affect[:-characters_to_remove]


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "covenin_data_scrapped.py")
    list_name = "covenin_elements_data"
    covenin_elements_lines = get_line_number_of_list_elements(file_path, list_name)

    essential_keys = ["nombre", "codigo_covenin", "unidad_de_medida", "categoria_revit"]
    allowed_categories = ["test", "example"]
    allowed_calc_metrics = ["m", "m2", "m3", "cantidad"]
    codes_storage = []
    names_storage = []

    error_msg = (
        "Los elementos que comienzan en las siguientes lineas contienen errores: "
    )
    left_keys_msg = "Falta nombre, codigo, unidad o categoría: "
    wrong_category_msg = "Categoría no permitida: "
    wrong_calc_metric_msg = "Cómputo métrico no permitido: "
    repeated_code_msg = "Código repetido: "
    repeated_name_msg = "Nombre repetido: "
    padding_msg = "    "

    left_keys_lines = ""
    wrong_category_lines = ""
    wrong_calc_metric_lines = ""
    repeated_code_lines = ""
    repeated_name_lines = ""

    for index, element in enumerate(covenin_elements_data):
        if all(key in element for key in essential_keys):
            if not element["codigo_covenin"] in codes_storage:
                codes_storage.append(element["codigo_covenin"])
            else:
                repeated_code_lines += f"{covenin_elements_lines[index]}, "

            if not element["nombre"] in names_storage:
                names_storage.append(element["nombre"])
            else:
                repeated_name_lines += f"{covenin_elements_lines[index]}, "

            if element["categoria_revit"] not in allowed_categories:
                wrong_category_lines += f"{covenin_elements_lines[index]}, "

            if element["unidad_de_medida"] not in allowed_calc_metrics:
                wrong_calc_metric_lines += f"{covenin_elements_lines[index]}, "

        else:
            left_keys_lines += f"{covenin_elements_lines[index]}, "

    # Check if there are errors and create the error message
    if (
        left_keys_lines
        or wrong_category_lines
        or wrong_calc_metric_lines
        or repeated_code_lines
        or repeated_name_lines
    ):
        error_msg += "\n"

        if not left_keys_lines == "":
            left_keys_lines = remove_last_characters(left_keys_lines, 2)
            error_msg += left_keys_msg + "\n" + padding_msg + left_keys_lines + "\n\n"

        if not wrong_category_lines == "":
            wrong_category_lines = remove_last_characters(wrong_category_lines, 2)
            error_msg += (
                wrong_category_msg + "\n" + padding_msg + wrong_category_lines + "\n\n"
            )

        if not wrong_calc_metric_lines == "":
            wrong_calc_metric_lines = remove_last_characters(wrong_calc_metric_lines, 2)
            error_msg += (
                wrong_calc_metric_msg
                + "\n"
                + padding_msg
                + wrong_calc_metric_lines
                + "\n\n"
            )

        if not repeated_code_lines == "":
            repeated_code_lines = remove_last_characters(repeated_code_lines, 2)
            error_msg += (
                repeated_code_msg + "\n" + padding_msg + repeated_code_lines + "\n\n"
            )

        if not repeated_name_lines == "":
            repeated_name_lines = remove_last_characters(repeated_name_lines, 2)
            error_msg += (
                repeated_name_msg + "\n" + padding_msg + repeated_name_lines + "\n\n"
            )

        print(error_msg)
    else:
        print("No hay errores en los elementos de la lista.")
