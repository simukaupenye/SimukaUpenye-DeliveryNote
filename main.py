import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
from fpdf import FPDF
import win32print
import win32api

# ---------- CONSTANT SUPPLIER INFO ----------
SUPPLIER_NAME = "Simuka Upenye Pvt Ltd"
SUPPLIER_ADDRESS = "Rippling Waters Farm, Macheke"
SUPPLIER_PHONE = "078 519 5945"
SUPPLIER_EMAIL = "jcwattson@yahoo.com"

# ---------- CSV FILE PATHS ----------
CUSTOMERS_FILE = "customers.csv"
TRANSPORTERS_FILE = "transporters.csv"
PRODUCTS_FILE = "products.csv"

# ---------- LOAD DROPDOWN DATA ----------
def load_csv_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return [row[0] for row in csv.reader(csvfile) if row]

# ---------- MAIN APP ----------
class DeliveryNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simuka Upenye Delivery Note")
        self.root.geometry("700x700")

        self.create_form()

    def create_form(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Supplier Header
        ttk.Label(frame, text=SUPPLIER_NAME, font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4)
        ttk.Label(frame, text=SUPPLIER_ADDRESS).grid(row=1, column=0, columnspan=4)
        ttk.Label(frame, text=f"Phone: {SUPPLIER_PHONE} | Email: {SUPPLIER_EMAIL}").grid(row=2, column=0, columnspan=4, pady=(0, 10))

        ttk.Separator(frame, orient="horizontal").grid(row=3, column=0, columnspan=4, sticky="ew", pady=5)

        # Customer
        ttk.Label(frame, text="Customer:").grid(row=4, column=0, sticky="e")
        self.customer_var = tk.StringVar()
        self.customer_cb = ttk.Combobox(frame, textvariable=self.customer_var, values=load_csv_data(CUSTOMERS_FILE))
        self.customer_cb.grid(row=4, column=1, sticky="w")

        # Transporter
        ttk.Label(frame, text="Transporter:").grid(row=5, column=0, sticky="e")
        self.transporter_var = tk.StringVar()
        self.transporter_cb = ttk.Combobox(frame, textvariable=self.transporter_var, values=load_csv_data(TRANSPORTERS_FILE))
        self.transporter_cb.grid(row=5, column=1, sticky="w")

        # Driver Info
        ttk.Label(frame, text="Driver Name:").grid(row=6, column=0, sticky="e")
        self.driver_name = ttk.Entry(frame)
        self.driver_name.grid(row=6, column=1)

        ttk.Label(frame, text="Driver ID:").grid(row=6, column=2, sticky="e")
        self.driver_id = ttk.Entry(frame)
        self.driver_id.grid(row=6, column=3)

        # Vehicle Info
        ttk.Label(frame, text="Truck Reg:").grid(row=7, column=0, sticky="e")
        self.truck_reg = ttk.Entry(frame)
        self.truck_reg.grid(row=7, column=1)

        ttk.Label(frame, text="Trailer Reg:").grid(row=7, column=2, sticky="e")
        self.trailer_reg = ttk.Entry(frame)
        self.trailer_reg.grid(row=7, column=3)

        ttk.Separator(frame, orient="horizontal").grid(row=8, column=0, columnspan=4, sticky="ew", pady=10)

        # Product Details
        ttk.Label(frame, text="Product:").grid(row=9, column=0, sticky="e")
        self.product_var = tk.StringVar()
        self.product_cb = ttk.Combobox(frame, textvariable=self.product_var, values=load_csv_data(PRODUCTS_FILE))
        self.product_cb.grid(row=9, column=1)

        ttk.Label(frame, text="Quantity:").grid(row=9, column=2, sticky="e")
        self.quantity = ttk.Entry(frame)
        self.quantity.grid(row=9, column=3)

        ttk.Label(frame, text="Type:").grid(row=10, column=0, sticky="e")
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=10, column=1)

        ttk.Label(frame, text="Destination:").grid(row=10, column=2, sticky="e")
        self.destination = ttk.Entry(frame)
        self.destination.grid(row=10, column=3)

        ttk.Label(frame, text="Description:").grid(row=11, column=0, sticky="e")
        self.description = ttk.Entry(frame, width=50)
        self.description.grid(row=11, column=1, columnspan=3, sticky="we")

        # Buttons
        ttk.Button(frame, text="Save & Print", command=self.save_and_print).grid(row=12, column=1, pady=15)
        ttk.Button(frame, text="New Delivery Note", command=self.reset_form).grid(row=12, column=2, pady=15)

    # ---------- SAVE & PRINT ----------
    def save_and_print(self):
        customer = self.customer_var.get()
        if not customer:
            messagebox.showerror("Error", "Please select a Customer.")
            return

        filename = f"DeliveryNote_{customer}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        # Header
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, SUPPLIER_NAME, ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, SUPPLIER_ADDRESS, ln=True, align="C")
        pdf.cell(0, 6, f"Phone: {SUPPLIER_PHONE} | Email: {SUPPLIER_EMAIL}", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "DELIVERY NOTE", ln=True, align="C")
        pdf.ln(8)

        # Info
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"Customer: {self.customer_var.get()}", ln=True)
        pdf.cell(0, 6, f"Transporter: {self.transporter_var.get()}", ln=True)
        pdf.cell(0, 6, f"Driver: {self.driver_name.get()} | ID: {self.driver_id.get()}", ln=True)
        pdf.cell(0, 6, f"Truck Reg: {self.truck_reg.get()} | Trailer Reg: {self.trailer_reg.get()}", ln=True)
        pdf.cell(0, 6, f"Destination: {self.destination.get()}", ln=True)
        pdf.ln(6)

        # Product Table
        pdf.set_font("Arial", "B", 10)
        pdf.cell(60, 8, "Product", 1)
        pdf.cell(30, 8, "Quantity", 1)
        pdf.cell(40, 8, "Type", 1)
        pdf.cell(60, 8, "Description", 1, ln=True)

        pdf.set_font("Arial", "", 10)
        pdf.cell(60, 8, self.product_var.get(), 1)
        pdf.cell(30, 8, self.quantity.get(), 1)
        pdf.cell(40, 8, self.type_entry.get(), 1)
        pdf.cell(60, 8, self.description.get(), 1, ln=True)

        pdf.ln(20)
        pdf.cell(0, 8, "Transporter Signature: ____________________", ln=True)
        pdf.cell(0, 8, "Supplier Signature: ____________________", ln=True)

        pdf.output(filename)

        try:
            win32api.ShellExecute(0, "print", filename, None, ".", 0)
            messagebox.showinfo("Success", f"Saved and sent to printer:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not print automatically:\n{e}")

    # ---------- RESET FORM ----------
    def reset_form(self):
        for var in [self.customer_var, self.transporter_var, self.product_var]:
            var.set("")
        for entry in [self.driver_name, self.driver_id, self.truck_reg, self.trailer_reg,
                      self.quantity, self.type_entry, self.description, self.destination]:
            entry.delete(0, tk.END)

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryNoteApp(root)
    root.mainloop()
