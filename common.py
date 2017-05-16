NEW_KEYS_FOUND_MESSAGE = "Keys present in the new file which are not in the original file :"
OLD_KEYS_NOT_FOUND_MESSAGE = "Keys present in the original file which are not in the new file :"
DIFFERENCES_MESSAGE = "Differences found for keys :"
DIFFERENT_COLUMNS_MESSAGE = "{key} : columns {differences}"
NEW_LINE_LONGER_MESSAGE = "{key} : The line in the second file is longer"
NEW_LINE_SHORTER_MESSAGE = "{key} : The line in the second file is shorter"

class DifferencesInfo:
    def __init__(self):
        self.new_keys_found = []
        self.old_keys_not_found = []
        self.line_differences = {}

class LineDifferencesInfo:
    def __init__(self):
        self.different_columns = []
        self.longer_in_second_file = False
        self.shorter_in_second_file = False
    def __bool__(self):
        if self.different_columns:
            return True
        if self.longer_in_second_file:
            return True
        if self.shorter_in_second_file:
            return True
        return False

def compare(original_data, new_data):
    # Create differences info
    differences = DifferencesInfo()
    # Check if the same keys are present
    original_keys = set(original_data.keys())
    new_keys = set(new_data.keys())
    for key in new_keys.difference(original_keys):
        differences.new_keys_found.append(key)
    for key in original_keys.difference(new_keys):
        differences.old_keys_not_found.append(key)
    # Check each line
    for key in new_keys.intersection(original_keys):
        line_differences = LineDifferencesInfo()
        new_line = new_data[key]
        original_line = original_data[key]
        # If the lines don't have the same length
        if len(new_line) != len(original_line):
            if len(new_line) > len(original_line):
                line_differences.longer_in_second_file = True
            else:
                line_differences.shorter_in_second_file = True
        # Get the length of the shorter line
        min_length_line = min(len(new_line), len(original_line))
        # Compare the cells present in both lines
        line_differences.different_columns = [i for i in range(min_length_line) if new_line[i] != original_line[i]]
        if line_differences:
            differences.line_differences[key] = line_differences
    return differences

def generate_report(differences):
    res = ""
    res += NEW_KEYS_FOUND_MESSAGE + "\n"
    for key in differences.new_keys_found:
        res += "\t" + str(key) + "\n"
    res += OLD_KEYS_NOT_FOUND_MESSAGE+"\n"
    for key in differences.old_keys_not_found:
        res += "\t" + str(key) + "\n"
    res += (DIFFERENCES_MESSAGE) + "\n"
    for key, line_differences in differences.line_differences.items():
        if line_differences.longer_in_second_file:
            res += "\t"+NEW_LINE_LONGER_MESSAGE.format(key=key)+"\n"
        if line_differences.shorter_in_second_file:
            res += "\t"+NEW_LINE_SHORTER_MESSAGE.format(key=key)+"\n"
        if line_differences.different_columns:
            res += "\t"+DIFFERENT_COLUMNS_MESSAGE.format(key=key,differences=line_differences.different_columns)+"\n"
    return res
