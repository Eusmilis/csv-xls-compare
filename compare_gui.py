import os
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.scrolledtext as tk_scrolledtext
from compare_csv import get_data as get_data_csv
from compare_xls import get_data as get_data_xls
from common import compare, generate_report

FIRST_FILE_LABEL_MESSAGE = "First file :"
SECOND_FILE_LABEL_MESSAGE = "Second file :"
COMPARE_BUTTON_LABEL = "Compare"
KEY_COLUMNS_LABEL = "Key columns (separator ',') :"

SECOND_FILE_COLUMN_OFFSET = 10

class CsvComparer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.minsize(width=400, height=200)
        # Key columns information
        key_columns_label = tk.Label(self.window, text=KEY_COLUMNS_LABEL)
        key_columns_label.grid(row=0, column=0, sticky="w")
        self.key_columns_var = tk.StringVar()
        key_columns_entry = tk.Entry(self.window, textvariable=self.key_columns_var)
        key_columns_entry.grid(row=1, column=0, sticky="we")

        # First file information
        first_file_label = tk.Label(self.window, text=FIRST_FILE_LABEL_MESSAGE)
        first_file_label.grid(row=2, column=0, sticky="w")

        self.first_file_path_var = tk.StringVar()
        first_file_path_entry = tk.Entry(self.window, textvariable=self.first_file_path_var)
        first_file_path_entry.grid(row=3, column=0, sticky="we")
        first_file_browse_button = tk.Button(self.window, text="...", command=self.make_askopenfilename(self.first_file_path_var))
        first_file_browse_button.grid(row=3, column=1, sticky="w")

        # Second file information
        second_file_label = tk.Label(self.window, text=SECOND_FILE_LABEL_MESSAGE)
        second_file_label.grid(row=2, column=0+SECOND_FILE_COLUMN_OFFSET, sticky="w")

        self.second_file_path_var = tk.StringVar()
        second_file_path_entry = tk.Entry(self.window, textvariable=self.second_file_path_var)
        second_file_path_entry.grid(row=3, column=0+SECOND_FILE_COLUMN_OFFSET, sticky="we")
        second_file_browse_button = tk.Button(self.window, text="...", command=self.make_askopenfilename(self.second_file_path_var))
        second_file_browse_button.grid(row=3, column=1+SECOND_FILE_COLUMN_OFFSET, sticky="w")

        # Report frame
        self.report_field = tk_scrolledtext.ScrolledText(self.window, state=tk.DISABLED, borderwidth=3, relief="sunken")
        self.report_field.grid(row=4, column=0, columnspan=12, sticky="nsew")

        # Compare button
        compare_button = tk.Button(self.window, text=COMPARE_BUTTON_LABEL, command=self.compare)
        compare_button.grid(row=10, column=SECOND_FILE_COLUMN_OFFSET-1, sticky="sew")

        # Grid configuration
        tk.Grid.columnconfigure(self.window, 0, weight=1)
        tk.Grid.columnconfigure(self.window, 0+SECOND_FILE_COLUMN_OFFSET, weight=1)
        tk.Grid.rowconfigure(self.window, 4, weight=1)

    def make_askopenfilename(self, string_var):
        def askopenfilename():
            string_var.set(tk_filedialog.askopenfilename())
        return askopenfilename

    def clean_report_field(self):
        self.report_field.config(state=tk.NORMAL)
        self.report_field.delete(1.0, tk.END)
        self.report_field.config(state=tk.DISABLED)

    def insert_into_report_field(self, index, text):
        self.report_field.config(state=tk.NORMAL)
        self.report_field.insert(index, text)
        self.report_field.config(state=tk.DISABLED)

    def compare_csv(self, first_file_name, second_file_name, key_columns):
        self.clean_report_field()
        key_columns = [int(i.strip()) for i in key_columns.split(',')]
        # Get first dictionary
        first_data = get_data_csv(first_file_name, *key_columns)
        # Get second dictionary
        second_data = get_data_csv(second_file_name, *key_columns)
        # Compare
        differences = compare(first_data, second_data)
        # Report
        self.insert_into_report_field(tk.END, generate_report(differences))

    def compare_xls(self, first_file_name, second_file_name, key_columns):
        self.clean_report_field()
        first_data = get_data_xls(first_file_name, *key_columns)
        second_data = get_data_xls(second_file_name, *key_columns)
        differences = compare(first_data, second_data)
        self.insert_into_report_field(tk.END, generate_report(differences))

    def compare(self):
        try:
            first_file_name = self.first_file_path_var.get()
            second_file_name = self.second_file_path_var.get()
            if not first_file_name or not second_file_name:
                raise Exception("Both files must be provided\n")
            key_columns = self.key_columns_var.get()
            if not key_columns:
                raise Exception("Key columns must be provided\n")
            if os.path.splitext(first_file_name)[-1] == ".csv":
                self.compare_csv(first_file_name, second_file_name, key_columns)
            if os.path.splitext(first_file_name)[-1] in [".xls", ".xlsx"]:
                self.compare_xls(first_file_name, second_file_name, key_columns)
        except Exception as e:
            self.insert_into_report_field(tk.END, str(e))

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = CsvComparer()
    gui.run()
