import os
import shutil
import hashlib
import datetime
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog

# ==========================
# 7 CHANGES MARKED INSIDE CODE
# ==========================

# CHANGE 7 → Delete logging function
def log_delete_operation(file_path):  # CHANGE 7
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
            log_delete_operation(path)   # CHANGE 7
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

        self.root.iconbitmap("icon.ico")    # CHANGE 1 → Set window icon

        Label(root, text="Secure File Management System", font=("Arial", 18, "bold")).pack(pady=10)   # CHANGE 2 → Added title label

        self.fm = FileManager()
        self.analytics = Analytics()

        scroll = Scrollbar(root)               # CHANGE 3 → Added scrollbar
        scroll.pack(side=RIGHT, fill=Y)

        self.output = Text(root, height=10, width=60, yscrollcommand=scroll.set)
        self.output.pack(pady=10)
        scroll.config(command=self.output.yview)

        Button(root, text="Store File", command=self.store_file).pack(pady=5)
        Button(root, text="Delete File", command=self.delete_file).pack(pady=5)
        Button(root, text="View Files", command=self.view_files).pack(pady=5)
        Button(root, text="Show Analytics", command=self.show_analytics).pack(pady=5)

        Button(root, text="Clear Output", command=lambda: self.output.delete("1.0", END)).pack(pady=5)   # CHANGE 4 → Added clear output button

        root.configure(bg="#e6f2ff")   # CHANGE 5 → Changed background color

    def show_output(self, msg):
        self.output.delete("1.0", END)
        self.output.insert(END, msg)

        messagebox.showinfo("Result", msg)    # CHANGE 6 → Show popup message after actions

    def store_file(self):
        path = filedialog.askopenfilename()
        if path:
            if self.fm.store_file(path):
                self.show_output("File stored successfully!")
            else:
                self.show_output("Failed to store file.")

    def delete_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.fm.secure_folder)
        file_name = os.path.basename(file_path)
        if file_name:
            if self.fm.delete_file(file_name):
                self.show_output("File deleted successfully!")
            else:
                self.show_output("File not found.")

    def view_files(self):
        files = self.fm.list_files()
        msg = "\n".join(files) if files else "No files found."
        self.show_output(msg)

    def show_analytics(self):
        files = self.fm.list_files()
        summary = self.analytics.generate_summary(files)
        self.show_output(summary)


root = Tk()
FileManagerGUI(root)
root.mainloop()
