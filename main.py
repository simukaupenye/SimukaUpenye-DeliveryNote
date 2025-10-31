import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from fpdf import FPDF
import os

# Permanent Supplier Info
SUPPLIER_NAME = "Simuka Upenye Pvt Ltd"
SUPPLIER_ADDRESS = "Rippling Waters Farm, Macheke"
SUPPLIER_PHONE = "078 519 5945"
SUPPLIER_EMAIL = "jcwattson@yahoo.com"

CSV_FILE = "delivery_records.csv"

class DeliveryNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simuka Upenye Delivery Note Entry Form")
        self.root.geometry("700x650")

        # Create form labels and entries
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        title = tk.Label(frame, text="Delivery Note Entry Form", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Define fields
        self.fields = {
            "Customer Name": tk.StringVar(),
            "Delivery Address": tk.StringVar(),
            "Product": tk.StringVar(),
            "Quantity": tk.StringVar(),
            "Type (e.g. Bag, Ton)": tk.StringVar(),
            "Transporter Name": tk.StringVar(),
            "Driver Name": tk.StringVar(),
            "Driver ID": tk.StringVar(),
            "Truck Reg": tk.StringVar(),
            "Trailer Reg": tk.StringVar()
        }

        # Dropdown options (CSV will auto-update if edited later)
        product_options = ["Maize", "Fertilizer", "Seed", "Wheat", "Sugar Beans"]
        type_options = ["Bag", "Ton", "Litre", "Box", "Crate"]

        # Create input fields
        row_num = 1
        for field, var in self.fields.items():
            label = tk.Label(frame, text=field + ":")
            label.grid(row=row_num, column=0, sticky="e", pady=3)

            if field == "Product":
                entry = ttk.Combobox(frame, textvariable=var, values=product_options, state="readonly")
            elif field == "Type (e.g. Bag, Ton)":
                entry = ttk.Combobox(frame, textvariable=var, values=type_options)
            else:
                entry = tk.Entry(frame, textvariable=var)

            entry.grid(row=row_num, column=1, pady=3, ipadx=50)
            row_num += 1

        # Buttons
        button_frame = tk.Frame(frame, pady=15)
        button_frame.grid(row=row_num, column=0, columnspan=2)

        tk.Button(button_frame, text="Save", command=self.save_data, width=20).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Print (PDF)", command=self.generate_pdf, width=20).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="New Delivery Note", command=self.clear_form, width=20).grid(row=0, column=2, padx=5)

    def save_data(self):
        data = [v.get() for v in self.fields.values()]
        if not all(data):
            messagebox.showerror("Error", "Please fill in all fields before saving.")
            return

        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(self.fields.keys())
            writer.writerow(data)
        messagebox.showinfo("Saved", "Data saved successfully to CSV file.")

    def generate_pdf(self):
        data = {k: v.get() for k, v in self.fields.items()}
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields before printing.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        customer_name = data["Customer Name"].replace(" ", "_")
        filename = f"DeliveryNote_{customer_name}_{timestamp}.pdf"

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # Title and Supplier Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, SUPPLIER_NAME, ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 6, SUPPLIER_ADDRESS, ln=True, align="C")
        pdf.cell(0, 6, f"Phone: {SUPPLIER_PHONE} | Email: {SUPPLIER_EMAIL}", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Delivery Note", ln=True, align="C")
        pdf.ln(8)

        pdf.set_font("Arial", "", 12)
        for key, value in data.items():
            pdf.cell(60, 8, f"{key}:", border=0)
            pdf.cell(0, 8, str(value), ln=True)

        pdf.ln(20)
        pdf.cell(0, 8, "__________________________", ln=True)
        pdf.cell(0, 6, "Transporter Signature", ln=True)
        pdf.ln(10)
        pdf.cell(0, 8, "__________________________", ln=True)
        pdf.cell(0, 6, "Supplier Signature", ln=True)

        pdf.output(filename)
        messagebox.showinfo("PDF Generated", f"PDF saved as '{filename}' in current directory.")

    def clear_form(self):
        for var in self.fields.values():
            var.set("")
        messagebox.showinfo("Reset", "Form cleared for a new delivery note.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryNoteApp(root)
    root.mainloop()
