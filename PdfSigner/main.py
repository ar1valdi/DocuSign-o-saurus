import tkinter as tk
import Encrypter
from tkinter import filedialog, messagebox


def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
    if file_path:
        pdf_label.config(text=file_path)
        app_state["pdf_path"] = file_path


def select_key():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki kluczy", "*.pem")])
    if file_path:
        key_label.config(text=file_path)
        app_state["key_path"] = file_path


def sign_pdf():
    pdf = app_state.get("pdf_path")
    key = app_state.get("key_path")
    if not pdf or not key:
        messagebox.showerror("Brak danych", "Wybierz zarówno plik PDF, jak i klucz prywatny.")
        return

    try:
        Encrypter.sign(pdf, key, "123")
        messagebox.showinfo("Sukces", "Plik PDF został poprawnie podpisany!")
    except Exception as e:
        messagebox.showerror("Wystąpił błąd: ", str(e))


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


app_state = {"pdf_path": str | None, "key_path": str | None}

root = tk.Tk()
root.title("Podpisywacz PDF")
root.geometry("1000x500")

pdf_btn = tk.Button(root, text="Wybierz plik PDF", command=select_pdf)
pdf_btn.pack(pady=10)
pdf_label = tk.Label(root, text="Nie wybrano pliku PDF")
pdf_label.pack()

key_btn = tk.Button(root, text="Wybierz klucz prywatny", command=select_key)
key_btn.pack(pady=10)
key_label = tk.Label(root, text="Nie wybrano klucza")
key_label.pack()

sign_btn = tk.Button(root, text="Podpisz PDF", command=sign_pdf)
sign_btn.pack(pady=10)

verify_btn = tk.Button(root, text="Weryfikuj PDF", command=verify_pdf)
verify_btn.pack(pady=10)

root.mainloop()
