import colour
import numpy as np
from colour import SDS_ILLUMINANTS





def clip_light_spectral(spectral_name_list, wave_range):
    """choose a list of standard illuminant, and get the 1-nm interval spectral data.
        (dict['wavelength_num'])

    Args:
        spectral_name_list (str_list): CIE illuminant name list. eg.['A', 'B', 'D50', 'D55', 'D60', 'D65', 'D75']
        wave_range (tupe): eg.(400, 700) will get [400nm, 700nm] 's data.
    """
    for i in spectral_name_list:
        light_spectral = SDS_ILLUMINANTS[i]
        light_spectral_clip = []
        for nm in range(wave_range[0], wave_range[1]+1):
            light_spectral_clip.append(light_spectral[str(nm)])
        # print(np.array(light_spectral_clip).shape)
        np.save(f'./data/spectral_{i}_{wave_range[0]}_{wave_range[1]}_1nm.npy', np.array(light_spectral_clip))


if __name__ == '__main__':
    
    name_list = ['A', 'B', 'D50', 'D55', 'D60', 'D65', 'D75']
    # name_list = ['D65']
    wave_range = (400, 700)
    clip_light_spectral(name_list, wave_range)

    # name = 'A'
    # light_spectral = SDS_ILLUMINANTS[name]
    # colour.plotting.plot_multi_sds([light_spectral])
    # print(light_spectral)
    # print(light_spectral[20:-16].shape)
    # print(light_spectral['400'])
    # print(light_spectral['700'])
    




    # res = colour.sd_to_XYZ(D65)
    # print(res)

