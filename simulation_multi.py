import numpy as np
import matplotlib.pyplot as plt
import smv_colour

from scipy import optimize
from simulate_sensor_color import SpectralColor
from utils.deltaE.deltaE_2000_np import delta_E_CIE2000
from utils.deltaE.deltaC_2000_np import delta_C_CIE2000



light_A = np.load("./data_illuminant/spectral_A_400_700_1nm.npy")
light_D75 = np.load("./data_illuminant/spectral_D75_400_700_1nm.npy")
xyz = np.load("./data/cam_1931-2-xyz_400-700_1nm.npy")


# cam1 = np.load("./data_cam_interp/camera_5_rgb_400_700_1nm.npy")
# cam2 = np.load("./data_cam_interp/camera_9_rgb_400_700_1nm.npy")
# cam3 = np.load("./cam_interp/camera_5_rgb_400_700_1nm.npy")

# cam12 = np.concatenate((cam1, cam2), axis=1)

# plt.figure(figsize=(30,10))
for i in range(12):
    cam1 = np.load(f"./data_cam_interp/camera_{i}_rgb_400_700_1nm.npy")


    def loss_func(x):
        x = x.reshape(-1, 3)
        calibration_xyz = np.dot(cam1, x)
        loss = ((calibration_xyz - xyz) ** 2).sum() ** 0.5
        # loss = abs(calibration_xyz - xyz).mean()
        return loss


    # x0 = np.random.rand(18)
    x0 = np.random.rand(9)
    res = optimize.minimize(loss_func, x0)
    # print(res.x)
    calibration_xyz = np.dot(cam1, res.x.reshape(-1, 3))

    # calibration_xyz *
    print((calibration_xyz * light_A[:, None]).sum(axis=0) / (xyz * light_A[:, None]).sum(axis=0))
    print((calibration_xyz * light_D75[:, None]).sum(axis=0) / (xyz * light_D75[:, None]).sum(axis=0))

    # print((calibration_xyz * light_D75[:, None]).sum(axis=0))
    # print((xyz * light_D75[:, None]).sum(axis=0))
    # exit()
    
    plt.figure(figsize=(30,8))
    color_list=['r', 'g', 'b']
    xyz_list = ['X', 'Y', 'Z']
    for j in range(3):
        plt.subplot(1, 3, j+1)
        plt.plot(calibration_xyz[:, j])
        plt.plot(xyz[:, j], c=color_list[j])
        plt.legend([f'calibrated_{xyz_list[j]}', f'{xyz_list[j]}'])
        plt.title(f'camera_{i}')
    plt.tight_layout()
    plt.show()


    # plt.figure()
    # plt.plot(calibration_xyz[:, 0])
    # # plt.plot(cam1[:, 0])
    # plt.plot(xyz[:, 0], c='r')
    # plt.xlabel('wavelength')
    # plt.title(f'camera_{i}')
    # plt.legend(['calibrated_x', "x"])

    # plt.figure()
    # plt.plot(calibration_xyz[:, 1])
    # # plt.plot(cam1[:, 1])
    # plt.plot(xyz[:, 1], c='g')
    # plt.xlabel('wavelength')
    # plt.title(f'camera_{i}')
    # plt.legend(['calibrated_y', "y"])


    # plt.figure()
    # plt.plot(calibration_xyz[:, 2])
    # # plt.plot(cam1[:, 2])
    # plt.plot(xyz[:, 2], c='b')
    # plt.xlabel('wavelength')
    # plt.title(f'camera_{i}')
    # plt.legend(['calibrated_z', "z"])

    # plt.show()


    ###=========================================================
    # sc = SpectralColor()
    # print(sc.spectral)

    # E_list = []
    # C_list = []
    # # for i in [sc.light_name_list[0], sc.light_name_list[-1]]:
    # for i in sc.light_name_list:
    #     print(f"========={i}========")

    #     # sensor = sc.cam4
    #     light = sc.light_spectral[i]
    #     checker = sc.colorchecker_1nm
    #     sensor_xyz = sc.cam_xyz
    #     sensor_calibrated_xyz = calibration_xyz

    #     assert len(sensor_xyz) == len(light) and checker.shape[-1] == len(light)

    #     realcolor = sc.color_integration(sensor_xyz, light, checker, interval=1)
    #     calibrated_color = sc.color_integration(sensor_calibrated_xyz, light, checker, interval=1)


    #     analog_gt = realcolor / 100.
    #     ideal_xyz = smv_colour.RGB2XYZ(analog_gt, 'bt709')
    #     ideal_lab = smv_colour.XYZ2Lab(ideal_xyz)

    #     analog_gt_tst = calibrated_color / 100.
    #     ideal_xyz_tst = smv_colour.RGB2XYZ(analog_gt_tst, 'bt709')
    #     ideal_lab_tst = smv_colour.XYZ2Lab(ideal_xyz_tst)

    #     res_deltaE = delta_E_CIE2000(ideal_lab, ideal_lab_tst)
    #     res_deltaC = delta_C_CIE2000(ideal_lab, ideal_lab_tst)

    #     print(res_deltaE)
    #     print(res_deltaC)
    #     E_list.append(res_deltaE.max())
    #     C_list.append(res_deltaC.max())
    
    # plt.plot(sc.light_name_list, E_list)
    # plt.plot(sc.light_name_list, C_list)
    # plt.legend(sc.light_name_list)

# plt.legend([f'camera_{i}' for i in range(12)])
# plt.xlabel('standard illuminant')
# plt.ylabel('max_deltaC00')
# plt.show()




    # np.save('./data/cam_1931-2-xyz_tst.npy', calibration_xyz)






# plt.figure()
# plt.plot(cam1)
# plt.plot(cam2)
# plt.show()

