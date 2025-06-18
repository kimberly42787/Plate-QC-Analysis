
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_data(df, safe_plate_name, s_b, z_prime):
    """
    Generate a QC plot (stripplot) of the control data with annotated QC metrics

    Parameters:
    - df (Dataframe): Dataframe containing the control data 
    - safe_plate_name (str): Filename-friendly plate name used for the title and filename
    - s_b (float): QC metric - Signal to bakcground ratio of the plate
    - z_prime (float): QC metric - Z-primer score indicating the assay quality

    Returns:
    - fig: Stripplot of the control data with annotated QC metrics 
    """

    fig = plt.figure(figsize=(4, 5.5))

    # Create a stripplot with the individual control values
    sns.stripplot(
        data = df,
        x = "Control_Type",
        y = "Value",
        jitter = 0.25,
        size = 8,
        palette = {"1mM FAC": "#013220", "Vehicle": "#DD8452"},
        alpha = 0.6
    )

    # Add a dashed median lines for the positive and negative control
    for idx, control_type in enumerate(["1mM FAC", "Vehicle"]):
        median_val = df[df["Control_Type"] == control_type]["Value"].median()
        plt.hlines (
            y = median_val,
            xmin = idx - 0.2,
            xmax = idx + 0.2, 
            color = "black", 
            linestyle = "--",
            linewidth = 2
        )
    
    # Set axis labels and plot title
    plt.ylim(0, 5)
    plt.ylabel("FL Ratio, Normalized to Vehicle")
    plt.margins(x = 0.25)
    plt.yticks(np.arange(0, 5, 1))
    plt.title(f"Plate QC - {safe_plate_name}")


    # Annotation text to show QC metrics
    annotation_text = f"S/B: {s_b:.3f}\nZ': {z_prime:.3f}"

    # Create the annotation box with the annotation_text (QC metrics)
    plt.gca().text(
        0.95, 0.95, 
        annotation_text, 
        transform = plt.gca().transAxes,
        fontsize = 11, 
        verticalalignment = "top",
        horizontalalignment = "right",
        bbox = dict(boxstyle = "round4, pad = 0.4",
                    facecolor = "#f9f9f9",
                    edgecolor = "black",
                    alpha = 0.70)
    )

    plt.tight_layout()
    return fig




