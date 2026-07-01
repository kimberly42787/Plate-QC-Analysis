
import pandas as pd

def safe_name(plate_name):
    """ 
    Convert plate name to a filename-friendly format by replacing spaces and slashes
    with underscores.

    Parameters:
    - plate_name (str): Original name of the plate taken from the raw dataframe
    
    Returns:
    - plate_name (str): Converted plate name that is safe for filenames.
    """
    return plate_name.replace(" ", "_").replace("/", "_")

def clean_plata_data(raw_df):
    """
    Clean the raw plate data by removing headers and footers, getting away with unnecessary
    columns, and converting values to numeric values which is used for the metric calculations

    Parameters: 
    - raw_df (Dataframe): Raw Dataframe including metadata and readings

    Returns: 
    - cleaned_df (Dataframe): Cleaned numeric data of the experiment run used to calculate
    QC metrics
    """
    
    # Skip the first two rows (headers and reset index)
    df = raw_df.iloc[2:].reset_index(drop=True)

    # Drop the first two columns 
    df = df.iloc[:, 2:]

    # Remove the last row 
    df = df.iloc[:-1]

    # Reassign column names to from 0 to N
    df.columns = range(df.shape[1])

    # Convert all the values to numberic
    cleaned_df = df.apply(pd.to_numeric, errors='coerce')
    
    return cleaned_df

def split_feor_hoechst(cleaned_df):
    """
    Split cleaned raw data into FeOR and Hoechst signal data

    Parameters:
    - cleaned_df (Dataframe): Cleaned dataframe for one plate run 

    Returns: 
    - feor, hoechst (tuple): Separated FeOR and Hoechst DataFrame
    """

    # Assign the first 12 columns as FeOR signals
    feor = cleaned_df.iloc[:, 0:12].reset_index(drop=True)

    # Assign columns 13-25 as Hoechst signals and re-index columns to match FeOR dataframe (0-11)
    hoechst = cleaned_df.iloc[:, 13:25].reset_index(drop=True)
    hoechst.columns = range(hoechst.shape[1])
    
    return feor, hoechst

def normalized_data(feor, hoechst):
    """
    Normalize FeOR/Hoechst ratio data by dividing by the average of the negatice control wells - cols 0 and 11

    Parameters: 
    - FeOR (Dataframe): FeOR signal data
    - Hoechst (Dataframe): Hoechst signal data

    Returns:
    - normalized_df (Dataframe): Normalized ratio values
    """

    # Calculate the FeOR/Hoechst ratio 
    ratio_df = feor / hoechst

    # Calculate the average of the negative controls (cols 0 and 11)
    control_ave = pd.concat([ratio_df.iloc[:, 0], ratio_df.iloc[:, 11]]).mean()

    # Normalize the entire ratio_df matrix by the control_ave
    normalized_df = ratio_df / control_ave
    
    return normalized_df

def controls(normalized_df):
    """
    Extract the positive and negative controls from the normalized data 

    Parameters: 
    - normalized_df (Dataframe): Normalized plate data

    Returns: 
    - pos_control, neg_control (tuple): Values for the positive and negative controls for the plate run
    """

    # Extract the positive control (this is assuming that it is located in column 10)
    pos_control = normalized_df.iloc[:, 10]

    # Extract the negative control (this is assuming that it is located in column 0 and 11)
    neg_control = pd.concat([normalized_df.iloc[:, 0], normalized_df.iloc[:, 11]])
    
    return pos_control, neg_control

def create_control_df(pos_control, neg_control, plate_name):
    """ 
    Create Dataframe containing the positive and negative control data for the plate run

    Parameters:
    - pos_control (Series): Values for the positive control (FAC)
    - neg_control (Series): Values for the negative control (Vehicle)
    - plate_name (str): Name of the plate run

    Returns: 
    - control_df (Dataframe): Dataframe of combined control data in a long format 
    """
    
    control_data = []

    # Label the positive controls 
    for val in pos_control:
        control_data.append(("1mM FAC", plate_name, val))

    # Label the negative controls
    for val in neg_control:
        control_data.append(("Vehicle", plate_name, val))

    # Create the Dataframe using the control data (positive and negative)
    control_df = pd.DataFrame(control_data, columns=["Control_Type", "Plate", "Value"])
    
    return control_df
