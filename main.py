import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ---------- Delivery Note Functions ----------
def save_delivery_note(customer, address, product, quantity, note_type):
    """Save delivery note to CSV."""
    filename = "delivery_notes.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Customer Name", "Address", "Product", "Quantity", "Type"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), customer, address, product, quantity, note_type])


def generate_pdf(customer, address, product, quantity, note_type):
    """Generate a printable PDF delivery note."""
    folder = "delivery_notes"
    os.makedirs(folder, exist_ok=True)

    pdf_filename = os.path.join(folder, f"DeliveryNote_{customer}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 800, "Simuka Upenye Delivery Note System")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 740, f"Customer: {customer}")
    c.drawString(50, 720, f"Address: {address}")
    c.drawString(50, 700, f"Product: {product}")
    c.drawString(50, 680, f"Quantity: {quantity}")
    c.drawString(50, 660, f"Type: {note_type}")

    c.line(50, 640, 550, 640)
    c.drawString(50, 620, "Received By: ______________________")
    c.drawString(300, 620, "Signature: ______________________")

    c.save()
    messagebox.showinfo("Printed", f"Delivery note saved to:\n{pdf_filename}")


# ---------- GUI ----------
def open_delivery_form(root):
    """Opens the delivery note form."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Delivery Note Entry Form", font=("Helvetica", 16, "bold")).pack(pady=10)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, sticky="e")
    customer_entry = tk.Entry(form_frame, width=30)
    customer_entry.grid(row=0, column=1, pady=3)

    tk.Label(form_frame, text="Delivery Address:").grid(row=1, column=0, sticky="e")
    address_entry = tk.Entry(form_frame, width=30)
    address_entry.grid(row=1, column=1, pady=3)

    tk.Label(form_frame, text="Product:").grid(row=2, column=0, sticky="e")
    product_entry = tk.Entry(form_frame, width=30)
    product_entry.grid(row=2, column=1, pady=3)

    tk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky="e")
    quantity_entry = tk.Entry(form_frame, width=30)
    quantity_entry.grid(row=3, column=1, pady=3)

    tk.Label(form_frame, text="Type (e.g. Bag, Ton):").grid(row=4, column=0, sticky="e")
    type_entry = tk.Entry(form_frame, width=30)
    type_entry.grid(row=4, column=1, pady=3)

    def on_submit():
        customer = customer_entry.get()
        address = address_entry.get()
        product = product_entry.get()
        quantity = quantity_entry.get()
        note_type = type_entry.get()

        if not all([customer, address, product, quantity, note_type]):
            messagebox.showerror("Error", "All fields are required!")
            return

        save_delivery_note(customer, address, product, quantity, note_type)
        messagebox.showinfo("Saved", "Delivery note saved successfully!")

    def on_print():
        customer = customer_entry.get()
        address = address_entry.get()
        product = product_entry.get()
        quantity = quantity_entry.get()
        note_type = type_entry.get()

        if not all([customer, address, product, quantity, note_type]):
            messagebox.showerror("Error", "All fields are required to print!")
            return

        generate_pdf(customer, address, product, quantity, note_type)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Save", command=on_submit, width=10).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Print", command=on_print, width=10).grid(row=0, column=1, padx=5)


def main():
    """App entry point."""
    root = tk.Tk()
    root.title("Simuka Upenye Delivery Note System")
    root.geometry("500x400")

    # Welcome Screen
    tk.Label(root, text="Welcome to Simuka Upenye Delivery Note System!",
             font=("Helvetica", 12)).pack(pady=100)

    root.after(1500, lambda: open_delivery_form(root))  # Automatically open form after 1.5s delay

    root.mainloop()


if __name__ == "__main__":
    main()
