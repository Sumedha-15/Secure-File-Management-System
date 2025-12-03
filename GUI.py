# ========================== # MODULE 1: GUI # ==========================
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from file_operations import FileManager
from analytics import Analytics

class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management System")
        self.root.geometry("600x400")

        # Change 1: Add window icon
        try:
            self.root.iconbitmap("")
        except:
            pass

        # Change 2: Add heading label
        tk.Label(root, text="Secure File Manager", font=("Arial", 16, "bold")).pack(pady=10)

        self.fm = FileManager()
        self.analytics = Analytics()

        self.path_var = tk.StringVar()
        tk.Label(root, text="Folder Path:").pack(pady=5)
        tk.Entry(root, textvariable=self.path_var, width=50).pack(pady=5)
        tk.Button(root, text="Browse", command=self.browse_folder).pack(pady=5)

        tk.Button(root, text="Create Folder", command=self.create_folder).pack(pady=5)
        tk.Button(root, text="Create File", command=self.create_file).pack(pady=5)
        tk.Button(root, text="Delete Item", command=self.delete_item).pack(pady=5)
        tk.Button(root, text="Rename Item", command=self.rename_item).pack(pady=5)
        tk.Button(root, text="Move Item", command=self.move_item).pack(pady=5)
        tk.Button(root, text="Search Files", command=self.search_files).pack(pady=5)
        tk.Button(root, text="Show Storage Usage", command=self.show_storage).pack(pady=5)

        self.result_box = tk.Text(root, height=8)
        self.result_box.pack(pady=10)

    # functions remain same...
