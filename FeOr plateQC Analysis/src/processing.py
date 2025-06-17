
import pandas as pd

# Turn the plate name into a safe name
def safe_name(plate_name):
    return plate_name.replace(" ", "_").replace("/", "_")

# Clean each plate raw data
def clean_plata_data(raw_df):
    df = raw_df.iloc[2:].reset_index(drop=True)
    df = df.iloc[:, 2:]
    df = df.iloc[:-1]
    df.columns = range(df.shape[1])
    cleaned_df = df.apply(pd.to_numeric, errors='coerce')
    return cleaned_df

# Split cleaned data by plata
def split_feor_hoechst(cleaned_df):
    feor = cleaned_df.iloc[:, 0:12].reset_index(drop=True)
    hoechst = cleaned_df.iloc[:, 13:25].reset_index(drop=True)
    hoechst.columns = range(hoechst.shape[1])
    return feor, hoechst

# Normalize data by the control average
def normalized_data(feor, hoechst):
    ratio_df = feor / hoechst
    control_ave = pd.concat([ratio_df.iloc[:, 0], ratio_df.iloc[:, 11]]).mean()
    normalized_df = ratio_df / control_ave
    return normalized_df

# Separate neg and pos controls
def controls(normalized_df):
    pos_control = normalized_df.iloc[:, 10]
    neg_control = pd.concat([normalized_df.iloc[:, 0], normalized_df.iloc[:, 11]])
    return pos_control, neg_control

# Create a dataframe from the controls 
def create_control_df(pos_control, neg_control, plate_name):
    control_data = []
    for val in pos_control:
        control_data.append(("1mM FAC", plate_name, val))
    for val in neg_control:
        control_data.append(("Vehicle", plate_name, val))

    # Create the Dataframe
    control_df = pd.DataFrame(control_data, columns=["Control_Type", "Plate", "Value"])
    return control_df
