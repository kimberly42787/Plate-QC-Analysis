# FerroOrange Plate QC Analyzer

A Python tool for automated QC analysis of 96-well plate-based FerroOrange assay. This pipeline extracts individual plates from a raw CSV export, cleans and normalizes fluorescence data, calculates critical assay performance metrics (Signal-to-Background, Z'-factor), and generates QC strip plots.

## Features
- Automatically splits raw multi-plate CSV into individual plate files
- Cleans and reshapes FeOR and Hoechst raw data
- Normalizes FeOr signal to Hoechst
- Calculates QC metrics:
  - Signal-to-Background (S/B) ratio
  - Z' Factor
- Generates individual plate strip plots for control visualization
- Outputs well-organized CSVs and PNG plots for presentation

## Built With: 

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=for-the-badge)


## Project Structure 
```bash
Plate-QC-Analysis/
├── src/
│   ├── main.py
│   ├── io_utils.py
│   ├── pipeline.py
│   ├── processing.py
│   ├── qc_metrics.py
│   └── qc_plotting.py
├── test/
│   ├── test_results/
│   └── test_file.csv
└── README.md
```

## Requirements

- Python 3.8+
- pandas
- numpy
- seaborn
- matplotlib
- tabulate

## Install via pip
```bash
pip install -r requirements.txt
```

## Logging
This project used Python's built-in logging module to:

- Track progress and key steps during plate processing
- Records warning and errors

## Metrics Explained
- Signal-to-Background (S/B):
  - Ratio of positive control signal to negative control background.

- Z'-factor:
  - Statistical measure of assay quality and separation between controls.

## Output: 
- Summary (Visualization)
  








           
