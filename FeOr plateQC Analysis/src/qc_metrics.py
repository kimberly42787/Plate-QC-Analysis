

# Calculate QC metrics
def calc_metric(pos_control, neg_control):
    pos_std = pos_control.std()
    neg_std = neg_control.std()
    pos_mean = pos_control.mean()
    neg_mean = neg_control.mean()

    s_b = pos_mean / neg_mean
    z_prime = 1 - ((3 * pos_std + 3 * neg_std) / abs(pos_mean - neg_mean))

    return s_b, z_prime
