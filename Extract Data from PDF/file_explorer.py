import tkinter as tk
from tkinter import filedialog

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()

    return file_paths

