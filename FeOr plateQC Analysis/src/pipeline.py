

import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from io_utils import raw_indices, create_directories
from processing import safe_name, clean_plata_data, split_feor_hoechst, normalized_data, controls, create_control_df
from qc_metrics import calc_metric
from qc_plotting import plot_data

# Configure logging
logging.basicConfig(
    level = logging.INFO,
    format= "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def process_plate(raw_file, output_folders):

    index_pairs = raw_indices(raw_file)

    results = {}

    # For loop to analyze raw plate data using the indices 
    for i, (start, end) in enumerate(index_pairs):
        try:
            # Extract plate name from the raw file and change plate name 
            plate_name = raw_file.iloc[start, 1] if pd.notna(raw_file.iloc[start, 1]) else f"Plate {i+1}"
            safe_plate_name = safe_name(plate_name)

            logger.info(f"Processing Plate {i+1} of {len(index_pairs)}: {safe_plate_name}")

            # Split each plate to be analyzed
            raw_plate = raw_file.iloc[start:end].reset_index(drop=True)
            results[safe_plate_name] = raw_plate

            # Save each plate to the plateRun folder
            plate_run_path = os.path.join(output_folders["plateRun"], f"{safe_plate_name}.csv")
            raw_plate.to_csv(plate_run_path, index=False)

            logger.info(f"Saved raw plate data for {safe_plate_name} to {plate_run_path}")

            # Clean and process data 
            clean_data = clean_plata_data(raw_plate)
            feor, hoechst = split_feor_hoechst(clean_data)
            norm_data = normalized_data(feor, hoechst)
            p_control, n_control = controls(norm_data)

            # Calculate QC metrics (Signal to Background and Z') and store data 
            s_b, z_prime = calc_metric(p_control, n_control)
            results[safe_plate_name] = {
                "Signal to Background:": s_b,
                "Z:": z_prime
            }

            logger.info(f"Calculated QC metrics for {safe_plate_name} -- S/B: {s_b:.3f}, Z: {z_prime:.3f}")

            # Save control data 
            control_df = create_control_df(p_control, n_control, plate_name)
            control_path = os.path.join(output_folders["controlsData"], f"{safe_plate_name}_controlData.csv")
            control_df.to_csv(control_path, index=False)

            logger.info(f"Control data for {safe_plate_name} is saved")

            # Plot data and save
            control_plot = plot_data(control_df, safe_plate_name, s_b, z_prime)
            plot_path = os.path.join(output_folders["qcPlots"], f"{safe_plate_name}_plot.png")
            control_plot.savefig(plot_path)

            logger.info(f"Control plot for {safe_plate_name} is saved!")
            plt.close(control_plot)

        except Exception as e:
            logger.error(f"Error processing Plate {plate_name}: {e}", exc_info=True)

    return results
