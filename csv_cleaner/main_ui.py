import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.loader import load_csv
from core.inspector import inspect_csv
from core.cleaner import (
    handle_missing_values,
    remove_duplicates,
    save_report,
    save_cleaned_csv,
    validate_column_types
)


class CSVCleanerUI:

    def __init__(self, root):
        self.root = root
        self.root.title("CSV Cleaner Tool")
        self.root.geometry("1440x1080")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_status_section()

        self.main_frame = ttk.Frame(root, padding=15)
        self.main_frame.pack(fill="both", expand=True)

        self.create_file_section()
        self.create_button_section()

        self.create_table_section()
        self.create_column_options_section()
        self.create_report_section()


    # ---------------- FILE SECTION ----------------
    def create_file_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding=10)
        frame.pack(fill="x", pady=5)

        ttk.Label(frame, text="Input CSV:").grid(row=0, column=0, sticky="w")

        self.input_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.input_var, width=70).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.load_file).grid(row=0, column=2)

        ttk.Label(frame, text="Output Folder:").grid(row=1, column=0, sticky="w")

        self.output_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.output_var, width=70).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.select_output).grid(row=1, column=2)

    # ---------------- BUTTON SECTION ----------------
    def create_button_section(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill="x", pady=10)

        self.clean_button = ttk.Button(frame, text="Clean Data", command=self.clean_data)
        self.clean_button.pack()

    # ---------------- TABLE SECTION ----------------
    def create_table_section(self):

        frame = ttk.LabelFrame(self.main_frame, text="Data Preview", padding=10)
        frame.pack(fill="both", expand=True)

        # Create container frame
        table_container = ttk.Frame(frame)
        table_container.pack(fill="both", expand=True)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_container, orient="vertical")
        x_scroll = ttk.Scrollbar(table_container, orient="horizontal")

        self.tree = ttk.Treeview(
            table_container,
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)

        # Layout
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    # ---------------- STATUS SECTION ----------------
    def create_status_section(self):
        self.status_var = tk.StringVar(value="Status: Ready")

        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x")

        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w"
        ).pack(fill="x")

    # ---------------- LOAD FILE ----------------
    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return

        self.input_var.set(filepath)
        self.status_var.set("Status: Loading CSV...")

        try:
            self.df = load_csv(filepath)

            report = inspect_csv(self.df)
            self.display_inspection_report(report)

            self.display_dataframe(self.df)

            self.dtype_dropdowns()
            self.missing_value_dropdowns()

            self.status_var.set("Status: File loaded successfully.")

        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("ERROR", f"Error: {e}")

    # ------------- REPORT SECTION --------------
    def create_report_section(self):

        report_frame = ttk.LabelFrame(self.main_frame, text="Reports", padding=10)
        report_frame.pack(fill="both", expand=True, pady=5)

        container = ttk.Frame(report_frame)
        container.pack(fill="both", expand=True)

        # ---------------- LEFT SIDE (Inspection) ----------------
        left_frame = ttk.LabelFrame(container, text="Inspection Report", padding=5)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.inspection_text = tk.Text(left_frame, wrap="none")
        self.inspection_text.pack(side="left", fill="both", expand=True)

        # SCROLLBAR for inspection
        inspection_scroll = ttk.Scrollbar(left_frame, command=self.inspection_text.yview)
        self.inspection_text.config(yscrollcommand=inspection_scroll.set)
        inspection_scroll.pack(side="right", fill="y")

        # ---------------- RIGHT SIDE (Cleaning) ----------------
        right_frame = ttk.LabelFrame(container, text="Cleaning Report", padding=5)
        right_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.cleaning_text = tk.Text(right_frame, wrap="none")
        self.cleaning_text.pack(side="left", fill="both", expand=True)

        # SCROLLBAR for cleaning
        cleaning_scroll = ttk.Scrollbar(right_frame, command=self.cleaning_text.yview)
        self.cleaning_text.config(yscrollcommand=cleaning_scroll.set)
        cleaning_scroll.pack(side="right", fill="y")

    def display_inspection_report(self, report):

        lines = []
        lines.append("*** CSV - Inspection Report ***")
        lines.append(f"Rows: {report['rows']}")
        lines.append(f"Columns: {report['columns']}")
        lines.append("\n---- Column Types ----")

        for col, val in report["data_types"].items():
            lines.append(f"{col}: {val}")

        lines.append("\n---- Missing Values ----")

        for col, val in report["missing_values"].items():
            lines.append(f"{col}: {val}")

        lines.append(f"\nDuplicate Values: {report['duplicate_values']}")

        self.inspection_text.delete("1.0", tk.END)
        self.inspection_text.insert(tk.END, "\n".join(lines))

    # ---------------- SELECT OUTPUT ----------------
    def select_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_var.set(folder)
            self.status_var.set("Status: Output folder selected.")

    # ---------------- CLEAN DATA ----------------
    def clean_data(self):

        if not hasattr(self, "df"):
            self.status_var.set("Error: No CSV loaded.")
            messagebox.showerror("ERROR","No CSV loaded.")
            return

        output_folder = self.output_var.get()
        if not output_folder:
            self.status_var.set("Error: Select output folder.")
            messagebox.showerror("ERROR","No output folder selected.")
            return

        try:
            df = self.df.copy()
            original_rows = len(df)

            # DATATYPE VALIDATION
            dtype_map = {}

            for col, var in self.dtype_vars.items():
                dtype_map[col] = var.get()

            df, conversion_report, dtype_changes = validate_column_types(df, dtype_map)

            # MISSING VALUES HANDLING
            missing_map = {}

            for col, var in self.missing_vars.items():
                missing_map[col] = var.get()

            df, filled_info = handle_missing_values(df, missing_map)

            df, duplicates = remove_duplicates(df)

            final_rows = len(df)

            # FILE NAMING
            original_filename = os.path.basename(self.input_var.get())
            base_name = os.path.splitext(original_filename)[0]

            cleaned_filename = f"{base_name}_cleaned.csv"
            report_filename = f"{base_name}_report.txt"

            cleaned_path = os.path.join(output_folder, cleaned_filename)
            report_path = os.path.join(output_folder, report_filename)

            # FILE SAVING
            save_cleaned_csv(df, cleaned_path)

            report_text = self.build_report(
                original_rows,
                final_rows,
                filled_info,
                len(duplicates),
                conversion_report,
                dtype_changes
            )

            self.display_cleaning_report(report_text)

            save_report(report_text, report_path)

            self.display_dataframe(df)

            self.status_var.set(f"Status: Saved {cleaned_filename} and {report_filename}.")
            messagebox.showinfo("SUCCESS", f"Cleaning Successful.\nsaved {cleaned_filename}\nsaved {report_filename}")

        except Exception as e:
            self.status_var.set(f"Error during cleaning: {e}")
            messagebox.showerror("ERROR", f"Error during cleaning: {e}")
    # ---------------- CLEANING REPORT --------------
    def display_cleaning_report(self, report_text):

        self.cleaning_text.delete("1.0", tk.END)
        self.cleaning_text.insert(tk.END, report_text)

    # ---------------- DISPLAY TABLE ----------------
    def display_dataframe(self, df):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    # ---------------- BUILD REPORT ----------------
    def build_report(self, original_rows, final_rows, filled_info, duplicate_count, conversion_report, dtype_changes):

        lines = []
        lines.append("DATA CLEANING REPORT")
        lines.append("--------------------")
        lines.append(f"Original rows: {original_rows}")
        lines.append(f"Final rows: {final_rows}")
        lines.append("")

        # DATA TYPE VALIDATION REPORT
        lines.append("")
        lines.append("Data Type Validation and Conversion:")

        if dtype_changes:
            for col, change in dtype_changes.items():
                lines.append(f"  {col} - {change}")
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Values changed to NaN while conversion:")

        if conversion_report:
            for col, count in conversion_report.items():
                lines.append(f"  {col} - {count}")
        else:
            lines.append("  None")

        # MISSING VALUE HANDLING REPORT
        lines.append("")
        lines.append("Missing values handling:")

        if not filled_info:
            lines.append("  None - No missing values handled")
        else:
            for col, (count, method) in filled_info.items():
                lines.append(f"  {col}\t: {count}\t- {method}")

        # DUPLICATE'S REPORT
        lines.append("")
        lines.append(f"Duplicate rows removed: {duplicate_count}")

        return "\n".join(lines)

    # -------------- COLUMN OPTIONS SECTION --------------
    def create_column_options_section(self):

        section_frame = ttk.LabelFrame(
            self.main_frame,
            text="Column Settings",
            padding=10
        )
        section_frame.pack(fill="x", pady=5)

        container = ttk.Frame(section_frame)
        container.pack(fill="both", expand=True)

        # ---------- LEFT SIDE (Datatype Selection) ----------
        self.dtype_frame = ttk.LabelFrame(
            container,
            text="Column Datatype Selection",
            padding=10
        )
        self.dtype_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Canvas for scrolling
        canvas = tk.Canvas(self.dtype_frame, height=120)

        scrollbar = ttk.Scrollbar(
            self.dtype_frame,
            orient="vertical",
            command=canvas.yview
        )

        self.dtype_container = ttk.Frame(canvas)

        self.dtype_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.dtype_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
        scrollbar.pack(side="right", fill="y")

        self.dtype_vars = {}

        # ------- RIGHT SIDE (Missing Value Handling) -------
        self.missing_frame = ttk.LabelFrame(
            container,
            text="Missing Value Handling",
            padding=10
        )
        self.missing_frame.pack(side="left", fill="both", expand=True, padx=5)

        canvas2 = tk.Canvas(self.missing_frame, height=120)

        scrollbar2 = ttk.Scrollbar(
            self.missing_frame,
            orient="vertical",
            command=canvas2.yview
        )

        self.missing_container = ttk.Frame(canvas2)

        self.missing_container.bind(
            "<Configure>",
            lambda e: canvas2.configure(scrollregion=canvas2.bbox("all"))
        )

        canvas2.create_window((0, 0), window=self.missing_container, anchor="nw")
        canvas2.configure(yscrollcommand=scrollbar2.set)

        canvas2.pack(side="left", fill="both", expand=True)
        canvas2.bind(
            "<MouseWheel>",
            lambda e: canvas2.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
        scrollbar2.pack(side="right", fill="y")

        self.missing_vars = {}


    def dtype_dropdowns(self):

        for widget in self.dtype_container.winfo_children():
            widget.destroy()

        self.dtype_vars = {}

        for col in self.df.columns:
            row = ttk.Frame(self.dtype_container)
            row.pack(fill="x", pady=2)

            ttk.Label(row, text=col, width=25).pack(side="left")

            dtype_var = tk.StringVar(value="string")

            dropdown = ttk.Combobox(
                row,
                textvariable=dtype_var,
                values=["string", "int", "float", "object"],
                state="readonly",
                width=10
            )

            dropdown.pack(side="left", padx=5)

            self.dtype_vars[col] = dtype_var

    def missing_value_dropdowns(self):

        # clear previous widgets
        for widget in self.missing_container.winfo_children():
            widget.destroy()

        self.missing_vars = {}

        for col in self.df.columns:
            row = ttk.Frame(self.missing_container)
            row.pack(fill="x", pady=2)

            ttk.Label(row, text=col, width=25).pack(side="left")

            method_var = tk.StringVar(value="None")

            dropdown = ttk.Combobox(
                row,
                textvariable=method_var,
                values=[
                    "None",
                    "Drop",
                    "Mean",
                    "Median",
                    "Mode",
                    "FFill",
                    "BFill"
                ],
                state="readonly",
                width=10
            )

            dropdown.pack(side="left", padx=5)

            self.missing_vars[col] = method_var


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVCleanerUI(root)
    root.mainloop()
