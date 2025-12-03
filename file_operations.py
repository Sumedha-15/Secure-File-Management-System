# ==========================
# MODULE 2: FILE OPERATIONS / BACKEND
# ==========================

import os
import shutil

class FileManager:
    def __init__(self):
        pass

    # Create a new folder
    def create_folder(self, path, folder_name):
        try:
            os.makedirs(os.path.join(path, folder_name), exist_ok=True)
            return f"Folder '{folder_name}' created successfully."
        except Exception as e:
            return str(e)

    # Create a new file
    def create_file(self, path, file_name):
        try:
            with open(os.path.join(path, file_name), 'w') as f:
                f.write("")  # empty file
            return f"File '{file_name}' created successfully."
        except Exception as e:
            return str(e)

    # Delete file or folder
    def delete_item(self, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                return "File deleted successfully."
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return "Folder deleted successfully."
            else:
                return "Path does not exist."
        except Exception as e:
            return str(e)

    # Rename file or folder
    def rename_item(self, path, new_name):
        try:
            base = os.path.dirname(path)
            os.rename(path, os.path.join(base, new_name))
            return "Renamed successfully."
        except Exception as e:
            return str(e)

    # Move file or folder
    def move_item(self, source, destination):
        try:
            shutil.move(source, destination)
            return "Moved successfully."
        except Exception as e:
            return str(e)

    # Search files in folder
    def search_files(self, path, keyword):
        try:
            result = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if keyword.lower() in file.lower():
                        result.append(os.path.join(root, file))
            return result
        except Exception as e:
            return str(e)
