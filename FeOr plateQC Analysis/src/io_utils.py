import os
import pandas as pd

def create_directories(parent_dir, sub_folders, run_folder=None):
    if run_folder is None:
        run_folder = input("Enter a folder name for this run:")
    
    base_dir = os.path.join(parent_dir, run_folder)
    os.makedirs(base_dir, exist_ok=True)

    sub_dir = {}

    for folder in sub_folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        sub_dir[folder] = path

    return sub_dir

# Get the indices of where each plate data starts
def raw_indices(raw_df):
    start_indices = raw_df.index[raw_df.iloc[:, 0] == "Plate:"].tolist()
    end_indices = raw_df.index[raw_df.iloc[:, 0] == "~End"].tolist()
    if len(start_indices) != len(end_indices):
        raise ValueError("Number of indices doesn't match each other")
    return list(zip(start_indices, end_indices))


