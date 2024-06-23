from .sample_for_macro import Sample_For_Macro as SFM
import os

class Measurement:
    def __init__(self, filename, *samples, time_delay_after_samples=None):
    #     try:
    #         os.remove(filename)  # delete it
    #     except FileNotFoundError as fe:
    #         print(fe)
        with open(filename, 'w') as fp:
            # pass

            for s in samples:
                s.write_to_file(filename)



        return

def main():
    configs = {'21':100}
    bp = (4,10)
    macro_name = '2023-01-18_2.mac'
    # try:
    #     os.remove(macro_name) #delete it
    # except FileNotFoundError as fe:
    #     print(fe)

    configs = {'21': 400, '22': 1000, '24': 2000}
    bp = (4,11)
    cy = (2,30)
    kapton  = SFM('kapton', configs, pos = (4,10), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha02 = SFM('dmcha02', configs, pos = (4,9), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha03 = SFM('dmcha03', configs, pos = (4,8), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha04 = SFM('dmcha04', configs, pos = (4,7), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha05 = SFM('dmcha05', configs, pos = (4,6), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha06 = SFM('dmcha06', configs, pos = (4,5), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha07 = SFM('dmcha07', configs, pos = (4,4), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha08 = SFM('dmcha08', configs, pos = (4,3), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha09 = SFM('dmcha09', configs, pos = (4,2), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)

    m = Measurement(macro_name, kapton, dmcha09, dmcha08, dmcha07, dmcha06, dmcha05, dmcha04, dmcha03, dmcha02)

    return

if __name__ == '__main__':
    main()