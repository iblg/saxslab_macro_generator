import os

class sample_for_macro:
    def __init__(self,
                 filepath,
                 name,
                 configs,
                 loc = None,
                 pos = None,
                 thickness = None,
                 blankloc = (0,0),
                 capscan = False,
                 transmission_measure = True,
                 align_beamstop = False):
        """
        filepath : str
            The path to the macro file that you will write this sample to. Before running this code, you must create an empty .mac file at the filepath.
        name : str
            The name of the sample. This is the name that will be recorded in the macro and the name of the data eventually measured.
        configs : dict
            Keys should be '1' '2' '3' '4' to choose the config (W,M,S,ES)AXS with 3 collimators, or '21' '22' '23' '24' for 2 collimators. Vals are measurement time in seconds.
        loc : tuple
            loc is the position of the sample, in mm. If both loc and pos are provided, loc is used.
        pos : tuple
            pos is the position of the sample in the SAXSLab ambient holder's coordinate units. If both loc and pos are provided, loc is used.
        thickness : float
            The thickness of the sample in centimeters.

            If thickness is provided, then the SAXSLab instrument will automatically correct for the sample thickness.
            However, this is not advisable for samples where a background will be taken.
        blankloc : tuple
            The position of the blank hole that is used for background subtraction and beamstop alignment, in mm.
        capscan : boolean
            Whether to align the sample using the built-in capillary alignment tools. Default is false.
        transmission_measure : boolean
            If true, the instrument will automatically take and subtract a dark frame and air scattering.
        align_beamstop : boolean
            If true, the instrument will automatically align the beamstop before measuring.
        """
        self.name = name

        #verify that configs are correct:
        self.configs = self.get_configs(configs)
        self.thickness = thickness
        self.configs = configs
        self.blankpos = blankpos
        self.align_beamstop = align_beamstop

        
        if loc: #if pos is provided
            self.loc = loc
        elif pos:
            self.loc = self.get_loc(pos)
        else:
            print('Please provide a loc or a pos argument for sample {}'.format(self.name))

        self.capscan = capscan
        self.transmission_measure = transmission_measure
        return

    def write_to_file(self, filename):
        with open(filename, 'a') as file:
            file.write('\n \n \n \n \n############################################################\n')
            file.write('#Sample: {}\n'.format(self.name))
            file.write('#Sample location: {} \n'.format(self.loc))
            file.write('sample00 = \"{}\" \n'.format(self.name))
            file.write('thickness00 = {}\n'.format(self.thickness))

            if self.capscan:
                file.write('capalign ysam 3 40 1\n')

            #align
            for config, time in self.configs.items():
                # file.write('mv ysam {}\n'.format(self.blankpos[0]))
                # file.write('mv zsam {}\n'.format(self.blankpos[1]))
                file.write('current_config = {}\n'.format(config))
                file.write('conf_ugo current_config\n')

                if self.align_beamstop:
                    file.write('mv beam2bstop\n')

                file.write('mv ysam {}\n'.format(self.loc[0]))
                file.write('mv zsam {}\n'.format(self.loc[1]))

                if self.thickness is not None:
                    file.write('SAMPLE_THICKNESS = thickness00\n')  # always in cm

                if self.transmission_measure is True:
                    file.write('transmission_measure\n')

                file.write('SAMPLE_DESCRIPTION = sprintf(\"Sample: %s, Configuration = %i, Temp = %2.1f, Time=%i\", sample00, current_config, T, time())\n')
                file.write('use_bsmask\n')
                file.write('saxsmeasure {} \n'.format(time))

        return
    
    def get_loc(self, pos):
        loc = [0,0]

        loc[0] = -8. * pos[1] + 48.
        loc[1] = 8. * pos[0] - 24.

        return loc

    def get_configs(self, configs):
        allowed = ['1', '2', '3', '4', '21', '22', '23', '24']

        if isinstance(configs, dict):
            for key, val in configs.items():
                if key in allowed:
                    pass
                else:
                    print('Invalid configuration inside of config dict. Allowed configs are {}'.format(allowed))
        else:
            print('Config argument for sample {} is invalid type. Config must be a dict!'.format(self.name))

        for key, val in configs.items():
            if type(val) == 'float' or 'int':
                if val > 0:
                    pass
                else:
                    print('Measurement time of sample {} must be greater than zero seconds \n.'.format(self.name))
            else:
                print('Measurement time must be given as float or int!')

        return configs

if __name__ == '__main__':
    main()