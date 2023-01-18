from sample_for_macro import Sample_For_Macro as SFM
import os

def main():
    macro_name = 'test.mac'
    try:
        os.remove(macro_name) #delete it
    except FileNotFoundError as fe:
        print(fe)

    configs = {'21':60}
    # bl = (0,0)
    bp = (3,6)
    p = (3,10)
    cy = (2.1, 30)
    x = SFM(macro_name, 'kapton', configs,
            # loc = (-24., 0.),
            # blankloc = bl,
            pos = p,
            blankpos = bp,
            capscan_y = cy,
            transmission_measure = True,
            align_beamstop = False)


    x.write_to_file(macro_name)
    return

if __name__ == '__main__':
    main()