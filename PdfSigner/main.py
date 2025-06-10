## @file main.py
# @brief GUI for signing and verifying PDF files using RSA keys
# @details Uses the Encrypter module for cryptographic operations

import tkinter as tk
import Encrypter
from tkinter import filedialog, messagebox

## @brief Select a PDF file to sign or verify.
def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
    if file_path:
        pdf_label.config(text=file_path)
        app_state["pdf_path"] = file_path


## @brief Select a PEM key file (public/private).
def select_key():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki kluczy", "*.pem")])
    if file_path:
        key_label.config(text=file_path)
        app_state["key_path"] = file_path


def select_key_auto():
    #TODO: Implement
    pass


## @brief Choose output directory for signed PDF.
def select_out():
    out_path = filedialog.askdirectory()
    if out_path:
        out_label.config(text=out_path)
        app_state["out_path"] = out_path


## @brief Sign the selected PDF using selected private key and PIN.
def sign_pdf():
    pdf = app_state.get("pdf_path")
    key = app_state.get("key_path")
    out = app_state.get("out_path")
    pin = pin_var.get()
    if not pdf or not key or not out or not pin:
        messagebox.showerror("Brak danych", "Wybierz zarówno plik PDF, jak i klucz prywatny.")
        return

    try:
        Encrypter.sign(pdf, key, pin, out)
        messagebox.showinfo("Sukces", "Plik PDF został poprawnie podpisany!")
    except Exception as e:
        messagebox.showerror("Wystąpił błąd: ", str(e))


## @brief Verify the digital signature of the selected PDF.
def verify_pdf():
    pdf = app_state.get("pdf_path")
    key = app_state.get("key_path")
    if not pdf or not key:
        messagebox.showerror("Brak danych", "Wybierz zarówno plik PDF, jak i klucz prywatny.")
        return

    if not Encrypter.verify(pdf, key):
        messagebox.showerror("Błąd weryfikacji", "Weryfikacja nie powiodła się.")
    else:
        messagebox.showinfo("Sukces", "Weryfikacja pliku PDF zakończona powodzeniem!")


## GUI Initialization
root = tk.Tk()
pin_var = tk.StringVar()
app_state = {"pdf_path": str | None, "key_path": str | None, "out_path": str | None}

root.title("Podpisywacz PDF")
root.geometry("1000x500")

# UI Elements
pdf_btn = tk.Button(root, text="Wybierz plik PDF", command=select_pdf)
pdf_btn.pack(pady=10)
pdf_label = tk.Label(root, text="Nie wybrano pliku PDF")
pdf_label.pack()

key_btn = tk.Button(root, text="Wybierz klucz", command=select_key)
key_btn.pack(pady=10)
aut_key_btn = tk.Button(root, text="Załaduj klucz z pendrive", command=select_key_auto)
aut_key_btn.pack(pady=10)
key_label = tk.Label(root, text="Nie wybrano klucza")
key_label.pack()

out_btn = tk.Button(root, text="Wybierz lokalizację do zapisu", command=select_out)
out_btn.pack(pady=10)
out_label = tk.Label(root, text="Nie wybrano ścieżki")
out_label.pack()

entry_pin = tk.Label(root, text="Enter PIN", pady=10)
entry_pin.pack()
entry_pin = tk.Entry(root, textvariable=pin_var, show="*", width=20, justify="center", font=("Courier", 14))
entry_pin.pack()

sign_btn = tk.Button(root, text="Podpisz PDF", command=sign_pdf)
sign_btn.pack(pady=10)

verify_btn = tk.Button(root, text="Weryfikuj PDF", command=verify_pdf)
verify_btn.pack(pady=10)

root.mainloop()
