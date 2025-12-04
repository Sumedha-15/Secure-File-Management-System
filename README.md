# 🔐 Secure File Management System (Python + Tkinter)

A desktop-based Secure File Manager built using **Python**, **Tkinter**, and **Matplotlib**.  
This tool allows users to securely store, manage, analyze, and delete files within an isolated `secure_storage` directory.

---

## 🚀 Features

### **📁 File Operations**
- **Store File** – Choose any file from your system and copy it into the secure storage.
- **Delete File** – Delete a selected file from secure storage (automatically logs deletion).
- **View Files** – Display a list of all stored files.
- **Create File** – Create a new file (e.g., `notes.txt`) inside secure storage.
- **Create Folder** – Add a new folder inside secure storage.
- **Reset (Clear All)** – Deletes ALL files and folders inside secure storage.

---

## 📊 Analytics Module

The analytics module provides:

### **1️⃣ Summary**
- Total number of files
- Listing of all files

Displayed through a popup message.

### **2️⃣ Pie Chart (File Type Distribution)**
A visual pie chart showing how many files belong to each extension type:

Example:
- `.txt`
- `.png`
- `.pdf`
- `.mp3`  
etc.

Useful to understand storage composition.

---

## 🛡 Security Features

### ✔ **Deletion Logging**
Every deleted file is stored in `delete_log.txt` with:
- Timestamp  
- File path  

### ✔ **Checksum Generator (SHA-256)**
Used internally to ensure file integrity (optional use).

---

## 🧩 Tech Stack

| Component | Technology |
|----------|------------|
| GUI | Tkinter |
| Plotting | Matplotlib |
| File Operations | OS, Shutil |
| Hashing | hashlib |
| Logging | datetime |

---

## ▶️ How to Run

1. Install required library:
   ```sh
   pip install matplotlib
   ```
2. Run the Python file:
   ```sh
   python finalSystem.py
   ```

The app window will open with all controls.
