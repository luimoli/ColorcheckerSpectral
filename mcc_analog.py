import os, sys
from statistics import mode
import os
import torch
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
sys.path.append(os.path.abspath('../'))

import glob
import cv2
import numpy as np
# import cv2.cv2 as cv2
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw, ImageFont
import smv_colour



plt.figure()


loss_list = []
# blc_list = range(10)
# for i in blc_list:
cam_list = ['cam1', 'cam2', 'cam3']
spectral_name_list = ['A', 'B', 'D50', 'D55', 'D60', 'D65', 'D75']
for cam in cam_list:
    loss_list = []
    for light in spectral_name_list:
        analog_gt = np.float32(np.load("./data_analog/analog_gt.npy") / 1000)
        ideal_xyz = smv_colour.RGB2XYZ(analog_gt, 'bt709')
        ideal_lab = smv_colour.XYZ2Lab(ideal_xyz)
        ideal_lab = np.expand_dims(np.float64(ideal_lab), 1)

        # ideal_lab = np.float64(np.loadtxt("./data/babelcolor_lab_D50.csv", delimiter=','))
        # ideal_lab = np.expand_dims(np.float64(ideal_lab), 1)

    

        src_for_ccm = np.float32((np.load(f'./data_analog/analog_{cam}_{light}.npy') + 0) / 255.)
        rgb_gain = src_for_ccm[18].max(keepdims=True) / src_for_ccm[18]
        src_for_ccm = src_for_ccm * rgb_gain * (0.91 / src_for_ccm[18, :].max())
        print(f"{cam}_{light}_rgb_gain:", rgb_gain)
        src_for_ccm = np.float64(src_for_ccm[:, None, :])

        model = cv2.ccm_ColorCorrectionModel(src_for_ccm, ideal_lab, cv2.ccm.COLOR_SPACE_Lab_D65_2)
        model.setColorSpace(cv2.ccm.COLOR_SPACE_sRGB)
        model.setCCM_TYPE(cv2.ccm.CCM_4x3)
        model.setDistance(cv2.ccm.DISTANCE_CIE2000)
        model.setLinear(cv2.ccm.LINEARIZATION_GAMMA)
        model.setLinearGamma(1)
        model.setLinearDegree(3)
        # model.setSaturatedThreshold(0, 0.98)
        model.run()
        mask = model.getMask()
        print(mask.sum())
        loss_list.append(model.getLoss())
        print('loss:', model.getLoss())
        ccm = model.getCCM()
        # print('ccm:\n{}\n'.format(ccm))
        print(f'================================')
    plt.plot(spectral_name_list, loss_list, marker='o')
    
        

plt.legend(cam_list)
plt.xlabel('different standard illuminant')
plt.ylabel('mean deltaE00')
# plt.ylim((1.50, 1.51))
plt.show()

# mask = model.getMask()
# for i in range(len(mask)):
#     print(i, mask[i])
# print(model.getWeights())

# ccm = model.getCCM()
# print('ccm:\n{}\n'.format(ccm))
# loss = model.getLoss()
# print('loss:\n{}\n'.format(loss))
# print('ccm.sum(axis=0):', ccm.sum(axis=0))
# exit()

        