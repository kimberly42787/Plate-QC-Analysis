import os
import pandas as pd

def create_directories(parent_dir, sub_folders, run_folder=None):
    """
    Create a base folder and specified subfolders for data to be stored in for the experiment run. 

    Parameters: 
    - parent_dir (str): Path of the parent directory where the base folder for the experiment run 
    should be created.
    - sub_folders (list of str): List of subdirectory to create inside the base folder specific for 
    the data being stored.
    - run_folder (str): Name of the run folder. Prompts user input

    Returns: 
    - sub_dir (dict): It returns a dictionary mapping subfolder names to their path.
    """
    
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

def raw_indices(raw_df):
    """
    Identifies the start and end indices for each plate block in a raw CSV dataframe. This assumes
    that each plate block starts with a row where the cell cell is "Plate:" and ends with a row where
    first cell is "~End".

    Parameters: 
    - raw_df (Dataframe): Raw input dataframe containing data on one or more plates for the experiment.

    Returns: 
    - list of (start_index, end_index) pairs for each plate

    Raises: 
    - ValueError: Raises an error if the number of start and end markers does not match. 
    """
    
    start_indices = raw_df.index[raw_df.iloc[:, 0] == "Plate:"].tolist()
    end_indices = raw_df.index[raw_df.iloc[:, 0] == "~End"].tolist()
    if len(start_indices) != len(end_indices):
        raise ValueError("Number of indices doesn't match each other")
    return list(zip(start_indices, end_indices))


