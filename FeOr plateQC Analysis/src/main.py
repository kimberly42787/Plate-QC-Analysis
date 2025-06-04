
import os
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate 
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from functions import *

# Hide the Tk window
Tk().withdraw()

# Ask to select the csv file to be analyze
runFile = askopenfilename(
    title=f"Select the raw CSV file",
    filetypes=[("CSV files", "*.csv")]
)

# Check if a file was selected. If so, read csv file and assign to rawFile
if runFile: 
    rawFile = pd.read_csv(runFile, header=None)
    print(f"CSV file was successsfully loaded!")
else: 
    print(f"No file was selected.")

# Get the parent directory where experimental runs are to be stored
parentDir = askdirectory(title=f"Select the parent directory for this run to be stored")

if not parentDir:
    print(f"No directory selected!")
    exit()

# Get an input for the run directory
runDirectory = os.path.join(parentDir, input(f"Enter a folder name for the FeOr run"))

# Create the directory if it doesn't exist
os.makedirs(runDirectory, exist_ok=True)
print(f"Run directory created at: {runDirectory}")

# Create sub directories for analyzed data to be stored
outputFolders = createDirectories(runDirectory, ["plateRun", "controlsData", "qcPlots", "summary"], runFolder=None)

# Get the indices for where each plate run data starts and ends and assign to indexPairs
indexPairs = rawIndices(rawFile)

# Assign an empty dictionary for QC metrics to be stored in 
results = {}

# For loop to analyze raw plate data using the indices 
for i, (start, end) in enumerate(indexPairs):

    # Extract plate name from the raw file 
    plateName = rawFile.iloc[start, 1] if pd.notna(rawFile.iloc[start, 1]) else f"Plate {i+1}"

    # Change plateName to a safeName
    safePlateName = safeName(plateName)

    # Add a progress indicator to show which plate is being run 
    print(f"Processing Plate {i+1} of {len(indexPairs)}: {safePlateName}")

    # Split each plate to be analyzed
    rawPlate = rawFile.iloc[start:end].reset_index(drop=True)

    # Assign the plate to the plate name inside results 
    results[safePlateName] = rawPlate

    # Save each plate to the plateRun folder
    plateRunPath = os.path.join(outputFolders["plateRun"], f"{safePlateName}.csv"])

    # Transform into a csv file and save in the plateRun folder under the plate name
    rawPlate.to_csv(plateRunPath, index=False)

    # Clean data 
    cleanData = cleanPlateData(rawPlate)

    # Extract raw FeOr and Hoechst data 
    feor, hoechst = splitRawData(cleanData)

    # Normalize data 
    normData = normalizedData(feor, hoechst)

    # Extract the positive and negative controls
    pControl, nControl = controls(normData)

    # Calculate QC metrics (Signal to Background and Z')
    s_b, zPrime = calcQCMetric(pControl, nControl)

    # Store data for the plate into results
    results[safePlateName] = {
        "Signal to Background:": s_b,
        "Z:": zPrime
    }

    #Create a data frame for the controls
    controlDF = createControlDF(pControl, nControl, plateName)

    # Create the directory for the controls
    controlPath = os.path.join(outputFolders["controlsData"], f"{safePlateName}_controlData.csv")

    controlDF.to_csv(controlPath, index=False)

    # Create the plot for the controls
    controlPlot = plotControls(controlDF, safePlateName, s_b, zPrime)

    # Create a directory for the plot 
    plotPath = os.path.join(outputFolders["qcPlots"], f"{safePlateName}_plot.png")

    # Save the plot into the foler
    controlPlot.savefig(plotPath, transparent=True)

    # Close figure
    plt.close(controlPlot)

# Assign an empty list 
displayData = []

# Collect the QC metric data for each plate
for plateName, data in results.items():
    displayData.append([
        plateName,
        f"{data['Signal to Background:']:.3f}",   
        f"{data['Z:']:.3f}"
    ])

# Print summary in a tabular form
print("\n Summary Result:")
print(tabulate(displayData, header=["Compounds", "Signal to Background", "Z'"], tablefmt="grid"))

# Save as a CSV file
summaryDF = pd.DataFrame(displayData, columns=["Compounds", "Signal to Background", "Z'"])
summaryPath = os.path.join(outputFolders["summary"], "RunSummary.csv")
summaryDF.to_csv(summaryPath, index=False)