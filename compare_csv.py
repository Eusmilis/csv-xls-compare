from common import LineDifferencesInfo, DifferencesInfo, generate_report

CSV_SEPARATOR = ";"

def get_data(file_name, *key_columns):
    with open(file_name) as file:
        data = [line.split(CSV_SEPARATOR) for line in file]
    data = {tuple(line[i] for i in key_columns):line for line in data}
    return data

def print_report(differences):
    print(generate_report(differences))
