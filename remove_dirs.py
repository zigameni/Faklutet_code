# Script to remove programming dirs after I am done. 

import os
import shutil

# List of folder names to search for and delete
folders_to_delete = ['.idea', '.vscode', '.venv', 'node_modules']

def delete_folders(root_dir, folders_to_delete):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for folder in folders_to_delete:
            folder_path = os.path.join(dirpath, folder)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted: {folder_path}")
                except Exception as e:
                    print(f"Error deleting {folder_path}: {e}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    delete_folders(current_directory, folders_to_delete)

