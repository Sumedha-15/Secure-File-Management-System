# ==========================
# MODULE 3: ANALYTICS
# ==========================

import os
import matplotlib.pyplot as plt
from file_operations import FileManager

class Analytics:
    def __init__(self):
        self.fm = FileManager()

    # Get folder size in KB
    def folder_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size / 1024

    # Show storage usage pie chart
    def show_storage_usage(self, path):
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        sizes = [self.folder_size(os.path.join(path, f)) for f in folders]

        if not folders:
            print("No folders found for analytics.")
            return

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=folders, autopct='%1.1f%%', startangle=140)
        plt.title("Folder Storage Usage (KB)")
        plt.show()
