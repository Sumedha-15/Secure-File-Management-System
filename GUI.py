import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from file_operations import FileManager
from analytics import Analytics

class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management System")
        self.root.geometry("600x400")

        self.fm = FileManager()
        self.analytics = Analytics()

        # Path Entry
        self.path_var = tk.StringVar()
        tk.Label(root, text="Folder Path:").pack(pady=5)
        tk.Entry(root, textvariable=self.path_var, width=50).pack(pady=5)
        tk.Button(root, text="Browse", command=self.browse_folder).pack(pady=5)

        # Buttons for operations
        tk.Button(root, text="Create Folder", command=self.create_folder).pack(pady=5)
        tk.Button(root, text="Create File", command=self.create_file).pack(pady=5)
        tk.Button(root, text="Delete Item", command=self.delete_item).pack(pady=5)
        tk.Button(root, text="Rename Item", command=self.rename_item).pack(pady=5)
        tk.Button(root, text="Move Item", command=self.move_item).pack(pady=5)
        tk.Button(root, text="Search Files", command=self.search_files).pack(pady=5)
        tk.Button(root, text="Show Storage Usage", command=self.show_storage).pack(pady=5)

        self.result_box = tk.Text(root, height=8)
        self.result_box.pack(pady=10)

    # GUI Functions
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_var.set(folder_selected)

    def create_folder(self):
        folder_name = simpledialog.askstring("Input", "Enter Folder Name:")
        if folder_name:
            result = self.fm.create_folder(self.path_var.get(), folder_name)
            self.show_result(result)

    def create_file(self):
        file_name = simpledialog.askstring("Input", "Enter File Name (with extension):")
        if file_name:
            result = self.fm.create_file(self.path_var.get(), file_name)
            self.show_result(result)

    def delete_item(self):
        file_path = filedialog.askopenfilename(initialdir=self.path_var.get())
        if file_path:
            result = self.fm.delete_item(file_path)
            self.show_result(result)

    def rename_item(self):
        file_path = filedialog.askopenfilename(initialdir=self.path_var.get())
        new_name = simpledialog.askstring("Input", "Enter New Name:")
        if file_path and new_name:
            result = self.fm.rename_item(file_path, new_name)
            self.show_result(result)

    def move_item(self):
        source = filedialog.askopenfilename(initialdir=self.path_var.get())
        destination = filedialog.askdirectory()
        if source and destination:
            result = self.fm.move_item(source, destination)
            self.show_result(result)

    def search_files(self):
        keyword = simpledialog.askstring("Input", "Enter keyword to search:")
        if keyword:
            results = self.fm.search_files(self.path_var.get(), keyword)
            if results:
                self.show_result("\n".join(results))
            else:
                self.show_result("No files found.")

    def show_storage(self):
        self.analytics.show_storage_usage(self.path_var.get())

    def show_result(self, message):
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, str(message))


# --------------------------
# MAIN PROGRAM
# --------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerGUI(root)
    root.mainloop()
