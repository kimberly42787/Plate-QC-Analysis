
import os
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate 
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import logging

from pipeline import process_plate
from io_utils import create_directories

# Configure logging
logging.basicConfig(
    level = logging.INFO,
    format= "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

def main():
    try:
        # Hide the Tk window
        Tk().withdraw()

        # Prompt the user to select the raw CSV file for analysis
        run_file = askopenfilename(
            title=f"Select the raw CSV file",
            filetypes=[("CSV files", "*.csv")]
        )

        # Check if a file was selected. If so, read csv file and assign to a dataframe
        if run_file: 
            raw_file = pd.read_csv(run_file, header=None)
            logger.info(f"CSV file was successfully loaded!")
        else: 
            logger.error(f"No file was selected!")
            exit()

        # Prompt the user to select a parent directory for the analysis to be sotred
        parent_dir = askdirectory(title=f"Select the parent directory for this run to be stored")

        # Exit if no directory is selected
        if not parent_dir:
            print(f"No directory selected!")
            exit()

        # Create sub directories for storing processed data and results
        output_folders = create_directories(parent_dir, ["plateRun", "controlsData", "qcPlots", "summary"], run_folder=None)

        # Process plate
        results = process_plate(raw_file, output_folders)

        # Assign an empty list 
        display_data = []

        # Collect the QC metric data for each plate
        for plate_name, data in results.items():
            display_data.append([
                plate_name,
                f"{data['Signal to Background:']:.3f}",   
                f"{data['Z:']:.3f}"
            ])

        # Print summary in a tabular form
        summary_table = tabulate(display_data, headers=["Compounds", "Signal to Background", "Z'"], tablefmt="grid")
        logger.info(f"Summary Results:\n" + summary_table)


        # Save as a CSV file in the summary folder
        summary_df = pd.DataFrame(display_data, columns=["Compounds", "Signal to Background", "Z'"])
        summary_path = os.path.join(output_folders["summary"], "RunSummary.csv")
        summary_df.to_csv(summary_path, index=False)
        logger.info(f"Summary Results are saved to: {summary_path}")

    except Exception as e:
        logger.error(f"Error has occurred: {e}")


if __name__ == "__main__":
    main()