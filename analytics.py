# ==========================
# MODULE 3: ANALYTICS
# ==========================

import os
import matplotlib.pyplot as plt
from file_operations import FileManager

class Analytics:
    def __init__(self):
        self.fm = FileManager()

    # Get folder size in MB
    def folder_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size / (1024 * 1024)  # Convert to MB

    # Show storage usage pie chart with improvements
    def show_storage_usage(self, path, save=False):
        # Fetch folders
        folders = [
            f for f in os.listdir(path) 
            if os.path.isdir(os.path.join(path, f))
        ]

        if not folders:
            print("No folders found for analytics.")
            return

        # Calculate sizes
        sizes = [
            self.folder_size(os.path.join(path, f)) 
            for f in folders
        ]

        # Avoid 0-size pie chart errors
        sizes = [s if s > 0 else 0.01 for s in sizes]

        # Identify largest folder
        max_folder = folders[sizes.index(max(sizes))]
        print(f"Largest folder: {max_folder} ({max(sizes):.2f} MB)")

        # Generate pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=folders, autopct='%1.1f%%', startangle=140)
        plt.title("Folder Storage Usage (MB)")

        # Save or show chart
        if save:
            plt.savefig("storage_usage.png")
            print("Chart saved as storage_usage.png")
        else:
            plt.show()
