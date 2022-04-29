from traceback import print_tb
import matplotlib.pyplot as plt
import numpy as np
import colour


class SpectralColor:
    def __init__(self, cam_volume=1, light_volume=1, checker_volume=1):
        self.cam1 = np.float32(np.loadtxt('./data/cam1_bgr.csv', delimiter=','))[:, 1:] # (31, 3)
        self.cam2 = np.float32(np.loadtxt('./data/cam2_bgr.csv', delimiter=','))[:, 1:]
        self.cam3 = np.float32(np.loadtxt('./data/cam3_bgr.csv', delimiter=','))[:, 1:]

        self.cam_xyz_tst = np.load('./data/cam_1931-2-xyz_tst.npy')
        self.cam_xyz = np.load('./data/cam_1931-2-xyz_400-700_1nm.npy') #r-g-b #(N, 3)
        self.cam_volume = cam_volume

        self.colorchecker_1nm = np.load('./data_reflectance/ColorChecker_spectral_400-700_1nm.npy') #(24, 31)
        self.colorchecker_10nm = np.float32(np.loadtxt('./data_reflectance/ColorChecker_spectral_400-700_10nm.csv', delimiter=',')) #(24, 31)
        self.checker_volume = checker_volume

        self.light_name_list = ['A', 'B', 'D50', 'D55', 'D60', 'D65', 'D75']
        self.light_spectral =self.__illuminant_init__()

    def __illuminant_init__(self):
        dic = {}
        for name in self.light_name_list:
            spectral = self.normalize(np.load(f'./data_illuminant/spectral_{name}_400_700_1nm.npy'))
            dic[name] = spectral

        return dic
    
    def __businesssCamera_init__(self):
        pass

    def normalize(self, arr):
        return (arr - arr.min()) / (arr.max() - arr.min())

    def calc_ab(self, x1, y1, x2, y2):
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return a, b

    def color_integration(self, sensor, light, checker, waverange=(400, 700), interval=10):
        """integration to calculate color value.

        Args:
            sensor (arr): shape:[N,3]
            light (arr): shape:[N]
            checker (arr): shape:[24, N]
            waverange (tuple, optional): . Defaults to (400, 700).
            interval (int, optional): interval of waverange. Defaults to 10 nm.

        Returns:
            arr: shape:[24,3] , 3-channel's order follows sensor's.
        """
        curve = (sensor * light[..., None])[None] * checker[..., None] # shape:[24, N, 3]
        num_color, num_spectral, num_channel = curve.shape
        assert waverange[0] + (num_spectral-1) * interval == waverange[1]

        real_color = []
        for i in range(num_color):
            sum_area = np.zeros((num_channel))
            for j in range(num_spectral - 1):
                x1, x2 = waverange[0] + j * interval, waverange[0] + (j + 1) * interval
                y1, y2 = curve[i][j], curve[i][j + 1]
                a, b = self.calc_ab(x1, y1, x2, y2)
                area = 0.5 * a * x2**2 + b * x2 - 0.5 * a * x1**2 - b * x1
                sum_area = sum_area + area
            real_color.append(sum_area)
        real_color = np.array(real_color)

        return real_color





if __name__ == '__main__':
    sc = SpectralColor()
    # print(sc.spectral)

    for i in [sc.light_name_list[0], sc.light_name_list[-1]]:
        # sensor = sc.cam4
        light = sc.light_spectral[i]
        checker = sc.colorchecker_1nm
        sensor_xyz = sc.cam_xyz_tst
        assert len(sensor_xyz) == len(light) and checker.shape[-1] == len(light)

        realcolor = sc.color_integration(sensor_xyz, light, checker, interval=1)
        print(realcolor.shape)
        print(realcolor.max(), realcolor.min())
        # np.save(r'D:\Code\CailibrationChecker\data\analog\analog_A.npy', realcolor)
        np.save(f'./analog_xyz_color/analog_gt_{i}_tst.npy', realcolor)
        print(realcolor)




    # for i in sc.light_name_list:
    #     sensor = sc.cam4
    #     light = sc.light_spectral[i][::10]
    #     checker = sc.colorchecker_10nm
    #     sensor_xyz = sc.cam_xyz[::10][:, ::-1]

    #     assert len(sensor) == len(light) and checker.shape[-1] == len(sensor)
    #     # plt.figure()
    #     # plt.plot(sensor[:, 0] * light)
    #     # plt.plot(sensor[:, 1] * light)
    #     # plt.plot(sensor[:, 2] * light)
    #     # plt.plot()


    #     # plt.figure()
    #     # plt.plot(sensor_xyz[:, 0] * light)
    #     # plt.plot(sensor_xyz[:, 1] * light)
    #     # plt.plot(sensor_xyz[:, 2] * light)
    #     # plt.plot()
    #     # plt.show()

    #     # continue

    #     realcolor = sc.calccolor(sensor, light, checker)
    #     print(realcolor.shape)
    #     print(realcolor)
    #     # np.save(r'D:\Code\CailibrationChecker\data\analog\analog_A.npy', realcolor)
    #     np.save(f'./data_analog/analog_cam4_{i}.npy', realcolor)


    # sensor = sc.cam1
    # light = sc.spectral_A[::10][10:41]
    # checker = sc.colorchecker_10nm

    # # sensor = sc.cam_xyz
    # # light = sc.spectral_D65[100:401]
    # # checker = sc.colorchecker_1nm

    # assert len(sensor) == len(light) and checker.shape[-1] == len(sensor)
    # realcolor = sc.calccolor(sensor, light, checker)
    # print(realcolor.shape)
    # print(realcolor)
    # np.save(r'D:\Code\CailibrationChecker\data\analog\analog_A.npy', realcolor)

