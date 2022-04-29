import colour
import numpy as np

INTERVAL = 1  # Spectral bin size.
SHAPE = colour.SpectralShape(400, 700, INTERVAL)
CMFS_1_NAME = 'CIE 1931 2 Degree Standard Observer'

# CMFS_1 = colour.colorimetry.MSDS_CMFS[CMFS_1_NAME].align(SHAPE)
CMFS_1 = colour.colorimetry.MSDS_CMFS[CMFS_1_NAME]
# print(np.array(CMFS_1[:]))
print(CMFS_1)
colour.plotting.plot_multi_cmfs([CMFS_1])
