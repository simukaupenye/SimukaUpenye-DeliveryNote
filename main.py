import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import csv
import os
import datetime
import tempfile
import pandas as pd
import subprocess

# --- Constants ---
SUPPLIER_NAME = "Simuka Upenye Pvt Ltd"
SUPPLIER_ADDRESS = "Rippling Waters Farm, Macheke"
SUPPLIER_PHONE = "078 519 5945"
SUPPLIER_EMAIL = "jcwattson@yahoo.com"

CSV_FILE = "delivery_data.csv"

# --- Helper Functions ---
def load_dropdown_data():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Customer", "Transporter", "Driver", "TruckReg", "TrailerReg", "Product"])
        df.to_csv(CSV_FILE, index=False)
    df = pd.read_csv(CSV_FILE)
    return df

def update_csv(df, column, value):
    if value and value not in df[column].dropna().values:
        df.loc[len(df)] = [None] * len(df.columns)
        df.at[len(df) - 1, column] = value
        df.to_csv(CSV_FILE, index=False)

def print_pdf(pdf_path):
    try:
        if os.name == "nt":  # Windows
            os.startfile(pdf_path, "print")
        else:
            subprocess.run(["lp", pdf_path])
    except Exception as e:
        messagebox.showerror("Print Error", f"Could not print file:\n{e}")

# --- Main App ---
class DeliveryNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simuka Upenye Delivery Note System")
        self.root.geometry("600x600")
        
        self.df = load_dropdown_data()
        
        # Title
        tk.Label(root, text="Delivery Note Entry Form", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame for inputs
        form = tk.Frame(root)
        form.pack(pady=10)
        
        # Input Fields
        self.entries = {}
        fields = [
            ("Customer Name", "Customer"),
            ("Delivery Address", None),
            ("Transporter Name", "Transporter"),
            ("Driver Name", "Driver"),
            ("Driver ID", None),
            ("Truck Reg", "TruckReg"),
            ("Trailer Reg", "TrailerReg"),
            ("Product", "Product"),
            ("Quantity", None),
            ("Type (e.g. Bag, Ton)", None)
        ]
        
        for idx, (label_text, csv_field) in enumerate(fields):
            tk.Label(form, text=label_text + ":", anchor="w").grid(row=idx, column=0, sticky="w", pady=4, padx=10)
            entry = tk.Entry(form, width=40)
            entry.grid(row=idx, column=1, pady=4)
            self.entries[label_text] = (entry, csv_field)
            
            # Pre-fill dropdown-like behavior
            if csv_field:
                unique_values = sorted(self.df[csv_field].dropna().unique())
                if unique_values.any():
                    entry.bind("<Button-1>", lambda e, v=unique_values, ent=entry: self.show_dropdown(v, ent))
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Save", command=self.save_delivery_note, width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Print", command=self.print_delivery_note, width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="New Delivery Note", command=self.clear_form, width=20).grid(row=0, column=2, padx=5))
    
    def show_dropdown(self, values, entry):
        dropdown = tk.Toplevel(self.root)
        dropdown.title("Select Value")
        dropdown.geometry("250x200")
        
        lb = tk.Listbox(dropdown)
        lb.pack(fill=tk.BOTH, expand=True)
        for v in values:
            lb.insert(tk.END, v)
        
        def select_value(event=None):
            selection = lb.get(lb.curselection())
            entry.delete(0, tk.END)
            entry.insert(0, selection)
            dropdown.destroy()
        
        lb.bind("<Double-1>", select_value)
    
    def save_delivery_note(self):
        data = {label: entry.get().strip() for label, (entry, _) in self.entries.items()}
        missing = [label for label, val in data.items() if not val]
        if missing:
            messagebox.showerror("Error", f"Please fill in all fields:\n{', '.join(missing)}")
            return
        
        # Update CSV dropdown data
        for label, (entry, csv_field) in self.entries.items():
            if csv_field:
                update_csv(self.df, csv_field, entry.get().strip())
        
        # Save PDF
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data['Customer Name'].replace(' ', '_')}_{timestamp}.pdf"
        pdf_path = os.path.join(tempfile.gettempdir(), filename)
        
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, SUPPLIER_NAME, ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"{SUPPLIER_ADDRESS}", ln=True, align="C")
        pdf.cell(0, 6, f"Phone: {SUPPLIER_PHONE} | Email: {SUPPLIER_EMAIL}", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Delivery Note", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("Arial", "", 11)
        for key, value in data.items():
            pdf.cell(60, 8, f"{key}:", border=0)
            pdf.cell(0, 8, value, ln=True, border=0)
        
        pdf.ln(15)
        pdf.cell(0, 8, "Signatures:", ln=True)
        pdf.cell(90, 8, "Transporter Signature: ___________________", ln=False)
        pdf.cell(0, 8, "Supplier Signature: ___________________", ln=True)
        
        pdf.output(pdf_path)
        messagebox.showinfo("Saved", f"Delivery note saved to:\n{pdf_path}")
        self.last_pdf = pdf_path
    
    def print_delivery_note(self):
        if hasattr(self, "last_pdf") and os.path.exists(self.last_pdf):
            print_pdf(self.last_pdf)
        else:
            messagebox.showerror("Error", "Please save a delivery note first before printing.")
    
    def clear_form(self):
        for entry, _ in self.entries.values():
            entry.delete(0, tk.END)

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryNoteApp(root)
    root.mainloop()
