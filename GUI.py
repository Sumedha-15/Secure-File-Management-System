import os
import shutil
import hashlib
import datetime
from tkinter import *
from tkinter import messagebox, filedialog

# CHANGE 7 → Added delete logging function
def log_delete_operation(file_path):
    with open("delete_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - Deleted: {file_path}\n")


def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return "File Not Found"


class FileManager:
    def __init__(self):
        self.secure_folder = "secure_storage"
        if not os.path.exists(self.secure_folder):
            os.makedirs(self.secure_folder)

    def store_file(self, source):
        if os.path.exists(source):
            shutil.copy(source, self.secure_folder)
            return True
        return False

    def delete_file(self, file_name):
        path = os.path.join(self.secure_folder, file_name)
        if os.path.exists(path):
            os.remove(path)

            # CHANGE 7 → Log delete action here
            log_delete_operation(path)

            return True
        return False

    def list_files(self):
        return sorted(os.listdir(self.secure_folder))


class Analytics:
    def generate_summary(self, files):
        summary = f"Total Files: {len(files)}\n\nFile List:\n"
        for f in files:
            summary += f" - {f}\n"
        return summary


class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Manager")
        self.fm = FileManager()
        self.analytics = Analytics()

        Label(root, text="Secure File Management System", font=("Arial", 16)).pack()

        Button(root, text="Store File", command=self.store_file).pack(pady=5)
        Button(root, text="Delete File", command=self.delete_file).pack(pady=5)
        Button(root, text="View Files", command=self.view_files).pack(pady=5)
        Button(root, text="Show Analytics", command=self.show_analytics).pack(pady=5)

        root.configure(bg="#e6f2ff")

    def store_file(self):
        path = filedialog.askopenfilename()
        if path:
            if self.fm.store_file(path):
                messagebox.showinfo("Success", "File stored successfully!")
            else:
                messagebox.showerror("Error", "Failed to store file.")

    def delete_file(self):
        file_name = filedialog.askopenfilename(initialdir=self.fm.secure_folder)
        file_name = os.path.basename(file_name)
        if file_name:
            if self.fm.delete_file(file_name):
                messagebox.showinfo("Deleted", "File deleted successfully!")
            else:
                messagebox.showerror("Error", "File not found.")

    def view_files(self):
        files = self.fm.list_files()
        messagebox.showinfo("Files", "\n".join(files) if files else "No files found.")

    def show_analytics(self):
        files = self.fm.list_files()
        summary = self.analytics.generate_summary(files)
        messagebox.showinfo("Analytics Summary", summary)


root = Tk()
FileManagerGUI(root)
root.mainloop()
