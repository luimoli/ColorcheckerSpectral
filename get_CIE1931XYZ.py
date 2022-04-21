import colour
import numpy as np

INTERVAL = 5  # Spectral bin size.
SHAPE = colour.SpectralShape(400, 700, INTERVAL)

CMFS_1_NAME = 'CIE 1931 2 Degree Standard Observer'
CMFS_1 = colour.colorimetry.MSDS_CMFS[CMFS_1_NAME].align(SHAPE)
# colour.plotting.plot_multi_cmfs([CMFS_1])
# print(np.array(CMFS_1[:]))


from colour import SDS_ILLUMINANTS
D65 = SDS_ILLUMINANTS['LED-B1']
# print(D65)
colour.plotting.plot_multi_sds([D65])

# res = colour.sd_to_XYZ(D65)
# print(res)