import smv_colour
import numpy as np
import matplotlib.pyplot as plt

from utils.deltaE.deltaE_2000_np import delta_E_CIE2000

spectral_name_list = ['A']
for light in spectral_name_list:
    print(light)
    analog_gt = np.float32(np.load(f"./analog_xyz_color/analog_gt_{light}.npy") / 100)
    
    # print(analog_gt[16]*100)
    ideal_xyz = smv_colour.RGB2XYZ(analog_gt, 'bt709')
    ideal_lab = smv_colour.XYZ2Lab(ideal_xyz)

    analog_gt_tst = np.float32(np.load(f"./analog_xyz_color/analog_gt_{light}_tst.npy") / 1000)
    print(analog_gt_tst[16]*100)
    ideal_xyz_tst = smv_colour.RGB2XYZ(analog_gt_tst, 'bt709')
    ideal_lab_tst = smv_colour.XYZ2Lab(ideal_xyz_tst)

    res_deltaE = delta_E_CIE2000(ideal_lab, ideal_lab_tst)
    res_deltaC = delta_E_CIE2000(ideal_lab, ideal_lab_tst)

    print(res_deltaE)
    print(res_deltaE.max())
