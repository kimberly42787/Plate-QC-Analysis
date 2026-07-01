# 96-Well Plate QC Analyzer

## Overview

This project was built to automate quality control analysis for fluorescence-based 96-well plate assays.

When analyzing multiple plates, I found that the same steps were repeated every time: separating plate data from a raw instrument export, cleaning the data, calculating quality control metrics, and generating plots to evaluate assay performance. Doing this manually was repetitive and made it easy to introduce small mistakes.

I wrote this pipeline to automate those steps so every plate is processed consistently and the results are generated in a reproducible way.

> **Note:** This repository uses example/test data only. No proprietary data or internal company information is included.



## What the pipeline does

Given a raw CSV export from a plate reader, the pipeline will:

- Split multiple plates into individual datasets
- Clean and reshape fluorescence measurements
- Normalize signal using a reference channel
- Calculate common assay quality metrics
- Generate QC plots for each plate
- Export cleaned data and figures



## Why I built it

The goal was to automate this analysis process. 

Instead of copying data into spreadsheets and running calculations by hand, this pipeline performs the same workflow automatically every time. That makes the analysis faster, easier to reproduce, and less prone to human error.


## QC Metrics

### Signal-to-Background (S/B)

Measures how well the positive controls are separated from the negative controls.

### Z'-Factor

A commonly used assay quality metric that evaluates both signal separation and variability.

| Z' | Interpretation |
|----|----------------|
| > 0.5 | Excellent |
| 0–0.5 | Marginal |
| < 0 | Poor |



## Workflow

```text
Raw CSV Export
      │
      ▼
Split Plates
      │
      ▼
Clean Data
      │
      ▼
Normalize Signal
      │
      ▼
Calculate QC Metrics
      │
      ▼
Generate Plots
      │
      ▼
Export Results
```



## Technologies

- Python
- pandas
- NumPy
- matplotlib
- seaborn
- tabulate



## Project Structure

```text
Plate-QC-Analysis/
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── processing.py
│   ├── qc_metrics.py
│   ├── qc_plotting.py
│   └── io_utils.py
├── test/
│   ├── test_results/
│   └── test_file.csv
├── requirements.txt
└── README.md
```



## Output

The pipeline generates:

- Individual plate CSV files
- QC metrics for each plate
- Strip plots for visual inspection
- Clean data ready for downstream analysis



## Skills Demonstrated

This project highlights experience with:

- Python scripting
- Data cleaning
- Workflow automation
- Statistical calculations
- Data visualization
- Modular code organization
- Logging and error handling



## Future Improvements

Some ideas I'd like to add in the future:

- Interactive dashboard using Dash or Streamlit
- Batch summaries across multiple experiments
- Excel report generation
- Additional QC visualizations








           
