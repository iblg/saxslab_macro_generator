import os
from saxslab_macro_generator.sample_for_macro import Sample_For_Macro as SFM
from saxslab_macro_generator.measurement import Measurement

def main():
    macro_name = 'my_macro.mac' #define the filepath to your file

    configs = {'21': 400, '22': 1000, '24': 2000} #set measurement configs. See docstring for details. Here we are measuring on SAXS configuration for 400 sec, MAXS for 1000, and ESAXS for 2000.
    bp = (4,11) #set the blank position, in ambient holder coordinates. ###NOTE: mm coordinates are also available
    cy = (2,30) #set the capillary alignment settings. Here we are measuring starting 2 mm to the right of the ysam position and scanning 2 mm left, with 40 increments

    #create your Sample_For_Macro objects
    kapton  = SFM('kapton', configs, pos = (4,10), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha02 = SFM('dmcha02', configs, pos = (4,9), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)
    dmcha03 = SFM('dmcha03', configs, pos = (4,8), thickness = None, blankpos = bp, capscan_y = cy, transmission_measure = True, align_beamstop = True)

    # Create your Measurement object. The first argument is the file that you want to write the macro to. All subsequent arguments are the samples you want to include in the measurement.
    # It will write the macro to file automatically.
    m = Measurement(macro_name, kapton, dmcha03, dmcha02)
    return

if __name__ == '__main__':
    main()