import os
import shutil
import hashlib
import datetime
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog

# ==========================
# Logging for delete actions
# ==========================
def log_delete_operation(file_path):
    with open("delete_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - Deleted: {file_path}\n")

# ==========================
# Checksum calculation
# ==========================
def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return "File Not Found"

# ==========================
# File Manager Class
# ==========================
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

# ==========================
# Analytics Class
# ==========================
class Analytics:
    def generate_summary(self, files):
        summary = f"Total Files: {len(files)}\n\nFile List:\n"
        for f in files:
            summary += f" - {f}\n"
        return summary

# ==========================
# GUI Class
# ==========================
class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Manager")
        self.root.geometry("650x550")
        self.root.configure(bg="#e6f2ff")  # Background color

        # CENTERING FRAME
        self.main_frame = Frame(root, bg="#e6f2ff")
        self.main_frame.pack(expand=True, fill=BOTH)

        # Title
        self.title = Label(self.main_frame, text="Secure File Management System",
                           font=("Helvetica", 20, "bold"), bg="#e6f2ff", fg="#1a1a1a")
        self.title.pack(pady=15)

        # ======================
        # Scrollable Text Box (now on top)
        # ======================
        box_frame = Frame(self.main_frame, bg="#d9f0ff", bd=3, relief=GROOVE)
        box_frame.pack(pady=10, padx=20, fill=BOTH, expand=False)

        self.scroll = Scrollbar(box_frame)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.output = Text(box_frame, height=12, width=70, yscrollcommand=self.scroll.set,
                           font=("Helvetica", 12), bg="#f0f8ff", bd=0, wrap=WORD)
        self.output.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.config(command=self.output.yview)

        # Buttons Frame
        self.button_frame = Frame(self.main_frame, bg="#e6f2ff")
        self.button_frame.pack(pady=10)

        # Buttons
        self.buttons = []
        btn_texts = ["Store File", "Delete File", "View Files", "Show Analytics", "Clear Output"]
        btn_commands = [self.store_file, self.delete_file, self.view_files, self.show_analytics,
                        lambda: self.output.delete("1.0", END)]
        for text, cmd in zip(btn_texts, btn_commands):
            b = Button(self.button_frame, text=text, width=22, height=2,
                       bg="#3399ff", fg="white", font=("Helvetica", 12, "bold"),
                       activebackground="#1a75ff", activeforeground="white",
                       relief=RAISED, bd=4, command=cmd)
            b.pack(pady=5)
            b.bind("<Enter>", lambda e, b=b: b.configure(bg="#1a75ff"))  # Hover effect
            b.bind("<Leave>", lambda e, b=b: b.configure(bg="#3399ff"))
            self.buttons.append(b)

        self.fm = FileManager()
        self.analytics = Analytics()

    # -------------------------
    # GUI functions
    # -------------------------
    def show_output(self, msg):
        self.output.delete("1.0", END)
        self.output.insert(END, msg)
        messagebox.showinfo("Result", msg)

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


# ==========================
# RUN GUI
# ==========================
root = Tk()
FileManagerGUI(root)
root.mainloop()
