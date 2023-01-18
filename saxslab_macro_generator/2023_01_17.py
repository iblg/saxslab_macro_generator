import os
from saxslab_macro_generator import Sample_For_Macro as SFM

def main():
    macro_name = 'test.mac'
    try:
        os.remove(macro_name) #delete it
    except FileNotFoundError as fe:
        print(fe)


    # 21 = 2 aperture waxs, 22 = 2 aperture maxs, 23 = 2 aperture saxs, 24 = 2 aperture esaxs
    configs = {'21': 180}
    x1 = SFM(macro_name, 'kapton', configs, capscan_y = 5)


    x1.write_to_file(macro_name)

    return