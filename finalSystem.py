import os
import shutil
import hashlib
import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import messagebox, filedialog, simpledialog


# ============================
# LOG DELETE ACTION
# ============================
def log_delete_operation(file_path):
    with open("delete_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - Deleted: {file_path}\n")


# ============================
# CHECKSUM CALCULATOR
# ============================
def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return "File Not Found"


# ============================
# FILE MANAGER BACKEND
# ============================
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
            log_delete_operation(path)
            return True
        return False

    def list_files(self):
        return sorted(os.listdir(self.secure_folder))

    def create_folder(self, name):
        path = os.path.join(self.secure_folder, name)
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    def create_file(self, name):
        path = os.path.join(self.secure_folder, name)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")
            return True
        return False

    def clear_all(self):
        """Deletes all contents inside secure_storage but keeps the folder."""
        for item in os.listdir(self.secure_folder):
            path = os.path.join(self.secure_folder, item)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        return True


# ============================
# ANALYTICS MODULE
# ============================
class Analytics:
    def generate_summary(self, files):
        summary = f"Total Files: {len(files)}\n\nFile List:\n"
        for f in files:
            summary += f" - {f}\n"
        return summary

    def generate_pie_chart(self, folder_path):
        files = os.listdir(folder_path)

        if not files:
            messagebox.showinfo("Analytics", "No files to analyze.")
            return

        file_types = {}
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1

        labels = list(file_types.keys())
        sizes = list(file_types.values())

        if sum(sizes) == 0:
            messagebox.showinfo("Analytics", "No valid file types found.")
            return

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("File Type Distribution in Secure Storage")
        plt.axis("equal")
        plt.show()


# ============================
# GUI
# ============================
class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#d9eaff")

        self.fm = FileManager()
        self.analytics = Analytics()

        # Title
        Label(root, text="Secure File Management System",
              font=("Arial", 20, "bold"), bg="#d9eaff").pack(pady=15)

        # Output Box
        self.output = Text(root, height=12, width=100,
                           bg="#e8f1ff", fg="black", font=("Arial", 12))
        self.output.pack(pady=10)

        # Button Frame (vertical)
        btn_frame = Frame(root, bg="#d9eaff")
        btn_frame.pack(pady=10)

        # Add buttons (stacked vertically)
        self.add_button(btn_frame, "Store File", self.store_file)
        self.add_button(btn_frame, "Delete File", self.delete_file)
        self.add_button(btn_frame, "View Files", self.view_files)
        self.add_button(btn_frame, "Show Analytics", self.show_analytics)
        self.add_button(btn_frame, "Create Folder", self.create_folder)
        self.add_button(btn_frame, "Create File", self.create_file)
        self.add_button(btn_frame, "Reset (Clear All Files)", self.clear_all_files)
        self.add_button(btn_frame, "Clear Output", self.clear_output)

    # Reusable vertical button creator
    def add_button(self, frame, text, cmd):
        Button(frame, text=text, command=cmd, width=22, height=2,
               bg="#5ea3ff", fg="white", activebackground="#1f6feb",
               font=("Arial", 12, "bold")).pack(pady=6)

    def print_output(self, text):
        self.output.insert(END, text + "\n")
        self.output.see(END)

    def clear_output(self):
        self.output.delete(1.0, END)

    # File operations
    def store_file(self):
        path = filedialog.askopenfilename()
        if path and self.fm.store_file(path):
            self.print_output(f"Stored: {path}")
        else:
            messagebox.showerror("Error", "Failed to store file.")

    def delete_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.fm.secure_folder)
        if file_path:
            file_name = os.path.basename(file_path)
            if self.fm.delete_file(file_name):
                self.print_output(f"Deleted: {file_name}")
            else:
                messagebox.showerror("Error", "File not found.")

    def view_files(self):
        files = self.fm.list_files()
        self.print_output("\n".join(files) if files else "No files available.")

    def show_analytics(self):
        files = self.fm.list_files()
        summary = self.analytics.generate_summary(files)
        messagebox.showinfo("Analytics Summary", summary)

        if files:
            self.analytics.generate_pie_chart(self.fm.secure_folder)

    def create_folder(self):
        name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if name:
            if self.fm.create_folder(name):
                self.print_output(f"Folder Created: {name}")
            else:
                messagebox.showerror("Error", "Folder already exists.")

    def create_file(self):
        name = simpledialog.askstring("Create File", "Enter file name (example: notes.txt):")
        if name:
            if self.fm.create_file(name):
                self.print_output(f"File Created: {name}")
            else:
                messagebox.showerror("Error", "File already exists.")

    def clear_all_files(self):
        confirm = messagebox.askyesno("Confirm Reset",
                                      "Are you sure you want to delete ALL files and folders inside secure_storage?")
        if confirm:
            self.fm.clear_all()
            self.print_output("All files deleted. Storage reset.")
            self.clear_output()
            messagebox.showinfo("Reset", "Storage cleared successfully!")


# ============================
# RUN APP
# ============================
root = Tk()
FileManagerGUI(root)
root.mainloop()
