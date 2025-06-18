
def calc_metric(pos_control, neg_control):
    """
    Calculate the QC metrics for this experiment:
        - Signal to Background Ratio (positive control / negative control)
        - Z-prime (Statistical parameter to assess quality of an assay by quantifying
        the separation of positive and negative controls

    Parameters:
    - pos_control (Series): Signal values from the positive control wells (FAC)
    - neg_control (Series): Signal values from the negative control wells (Vehicle)

    Returns:
    - s_b, z_prime (tuple):
        - Values of s_b (float) and z_prime (float)
    """

    # Calculate the standard deviation of the positive and negative controls
    pos_std = pos_control.std()
    neg_std = neg_control.std()

    # Calculate the mean of the positive and negative controls
    pos_mean = pos_control.mean()
    neg_mean = neg_control.mean()

    # Calculate the signal to background ratio
    s_b = pos_mean / neg_mean

    # Calculate the Z-prime score 
    z_prime = 1 - ((3 * pos_std + 3 * neg_std) / abs(pos_mean - neg_mean))

    return s_b, z_prime
