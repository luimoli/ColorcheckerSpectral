import numpy as np 
from scipy import interpolate as inter
import matplotlib.pyplot as plt
from scipy import constants as Const



def spectral_inerp(spectral_arr, mode, start_stop, interval, interval_new):
    """make the interpolation of spectral data.

    Args:
        spectral_arr (arr): _description_
        mode (str): '0': colorchecker; shape:[24, n] 
                    '1': illuminant;   shape:[n]
                    '2': sensor spectral response; shape: [n, 3]
        start_stop (tuple): (400, 700) wavelength range
        interval (int): original interval (eg. 10 nm)
        interval_new (int): new interpolation interval (eg. 1 nm)

    Returns:
        _type_: _description_
    """
    if mode == '0' or mode == '1':
        assert spectral_arr.ndim <= 2
        if spectral_arr.ndim == 1:
            spectral_arr == spectral_arr[None].copy()

        index = np.arange(start_stop[0], start_stop[1]+1, interval)
        num_color = len(spectral_arr)
        color_list=[]
        for i in range(num_color):
            f = inter.interp1d(index, spectral_arr[i], kind ="cubic") 
            index_new = np.arange(start_stop[0], start_stop[1]+1, interval_new)
            spectral_arr_value_new = f(index_new)
            color_list.append(spectral_arr_value_new)
        spectral_arr_interp = np.array(color_list)
        print('mode', mode, ':', spectral_arr_interp.shape)
    
    elif mode == '2':
        index = np.arange(start_stop[0], start_stop[1]+1, interval)
        num_curve = spectral_arr.shape[-1]
        color_list=[]
        for i in range(num_curve):
            f = inter.interp1d(index, spectral_arr[:, i],kind ="cubic") 
            index_new = np.arange(start_stop[0], start_stop[1]+1, interval_new)
            spectral_arr_value_new = f(index_new)
            color_list.append(spectral_arr_value_new[..., None])
        spectral_arr_interp = np.concatenate(color_list, axis=-1)
        print('mode', mode, ':', spectral_arr_interp.shape)

    else:
        raise ValueError('mode error!')
    
    return spectral_arr_interp


if __name__ == '__main__':

    # spectral_arr = np.float32(np.loadtxt('./data/sensor1_rgb.csv', delimiter=','))
    # tst = spectral_inerp(spectral_arr[:, 1:], '2', (400, 700), 4, 1)

    # plt.figure()
    # plt.plot(np.arange(400, 701, 1), tst[:, 0], 'r')
    # plt.plot(np.arange(400, 701, 1), tst[:, 1], 'g')
    # plt.plot(np.arange(400, 701, 1), tst[:, 2], 'b')
    # # plt.xlim((400,700))
    # plt.legend(['r','g','b'])
    # plt.show()
    # np.save('./cam/'spectral_arr)

    for i in range(12):
        spectral_arr = np.float32(np.loadtxt(f'./cam/camera_{i}.spectra'))
        # print(type(spectral_arr), spectral_arr.shape)
        # exit()
        tst = spectral_inerp(spectral_arr[:, 1:], '2', (400, 700), 4, 1)

        plt.figure()
        plt.plot(np.arange(400, 701, 1), tst[:, 0], 'r')
        plt.plot(np.arange(400, 701, 1), tst[:, 1], 'g')
        plt.plot(np.arange(400, 701, 1), tst[:, 2], 'b')
        # plt.xlim((400,700))
        plt.legend(['r','g','b'])
        plt.xlabel('wavelength(nm)')
        plt.ylabel('spectral distribution')
        plt.title(f'camera_{i}')
        plt.show()
        np.save(f'./cam_interp/camera_{i}_rgb_400_700_1nm.npy', tst)


# colorchecker = np.float32(np.loadtxt('./data/ColorChecker_spectral_400-700_10nm.csv', delimiter=',')) #(24, 36)
# index = np.arange(400, 701, 10)
# num_color = len(colorchecker)
# color_list=[]
# for i in range(num_color):
#     f = inter.interp1d(index, colorchecker[i],kind ="cubic") 
#     index_new = np.arange(400, 701, 1)
#     colorchecker_value_new = f(index_new)
#     color_list.append(colorchecker_value_new)
# colorchecker_new = np.array(color_list)
# print(colorchecker_new.shape)
# plt.plot(index, colorchecker[18],'o',index_new, colorchecker_new[18],'-') 
# plt.legend(['data','inerp'], loc='best') 
# plt.show()
# np.save('./data/ColorChecker_spectral_400-700_1nm.npy', colorchecker_new)




# colorchecker = np.float32(np.loadtxt('./data/ColorChecker_spectral_400-700_10nm.csv', delimiter=',')) #(24, 36)
# index = np.arange(400, 701, 10)
# f = inter.interp1d(index, colorchecker[0],kind ="cubic") 
# index_new = np.arange(400, 701, 1)
# colorchecker_value_new = f(index_new)
# plt.plot(index, colorchecker[0],'o',index_new,colorchecker_value_new,'-') 
# plt.legend(['data','interp'], loc='best') 
# plt.show()