import qrcode
from PIL import Image
import sqlite3
import tkinter as tk
from tkinter import ttk

def create_database():
    conn = sqlite3.connect("qrcodes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        label TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def generate_qr_code(content, label):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    filename = f"{label}.png"
    qr_img.save(filename)

    return filename

def insert_qr_code_into_db(content, label):
    conn = sqlite3.connect("qrcodes.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO qr_codes (content, label) VALUES (?, ?)", (content, label))

    conn.commit()
    conn.close()

def retrieve_qr_codes_from_db():
    conn = sqlite3.connect("qrcodes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, content, label FROM qr_codes")
    qr_codes = cursor.fetchall()

    conn.close()

    return qr_codes

def generate_qr_code_handler():
    content = content_entry.get()
    label = label_entry.get()
    filename = generate_qr_code(content, label)
    insert_qr_code_into_db(content, label)
    result_label.config(text=f"Generated QR code for Label: {label}, Saved as: {filename}")

def view_qr_codes_handler():
    qr_codes_from_db = retrieve_qr_codes_from_db()
    result_text = ""
    for qr_code in qr_codes_from_db:
        id, content, label = qr_code
        filename = generate_qr_code(content, label)
        result_text += f"Generated QR code for ID: {id}, Label: {label}, Saved as: {filename}\n"
    result_label.config(text=result_text)

root = tk.Tk()
root.title("QR Code Generator and Manager")

content_label = tk.Label(root, text="Content:")
content_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

content_entry = tk.Entry(root)
content_entry.grid(row=0, column=1, padx=10, pady=5)

label_label = tk.Label(root, text="Label:")
label_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

label_entry = tk.Entry(root)
label_entry.grid(row=1, column=1, padx=10, pady=5)

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code_handler)
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

view_button = tk.Button(root, text="View Stored QR Codes", command=view_qr_codes_handler)
view_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

result_label = tk.Label(root, text="", wraplength=400, justify="left")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

create_database()

root.mainloop()