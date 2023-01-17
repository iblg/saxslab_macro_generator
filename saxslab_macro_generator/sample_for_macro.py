import os

class Sample_For_Macro:
    def __init__(self,
                 filepath,
                 name,
                 configs,
                 loc = None,
                 pos = None,
                 thickness = None,
                 blankloc = None,
                 blankpos = None,
                 capscan_y = False,
                 capscan_z = False,
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
        self.align_beamstop = align_beamstop


        
        if loc: #if pos is provided
            self.loc = loc
        elif pos:
            self.loc = self.get_loc(pos)
        else:
            print('Please provide a loc or a pos argument for sample {}'.format(self.name))

        if blankloc: #if blankloc is provided (i.e., in mm units)
            self.blankloc = blankloc
        elif blankpos: #if blankpos is provided (i.e., in AM-yy,zz units)
            self.blankloc = self.get_loc(blankpos)
        else:
            print('You did not provide a blank location in mm coordinates. Please provide a blank location.')

        self.capscan_y = capscan_y
        self.capscan_z = capscan_z
        self.transmission_measure = transmission_measure
        return

    def write_to_file(self, filename):
        with open(filename, 'a') as file:
            file.write('\n \n \n \n \n############################################################\n')
            file.write('#Sample: {}\n'.format(self.name))
            file.write('#Sample location: {} \n'.format(self.loc))
            file.write('sample00 = \"{}\" \n'.format(self.name))
            file.write('thickness00 = {}\n'.format(self.thickness))

            if self.blankloc:
                file.write('mv ysam {}\n'.format(self.blankloc[0]))
                file.write('mv zsam {}\n'.format(self.blankloc[1]))
                file.write('blankpos_def\n'.format(self.blankloc[1]))

            file.write('mv ysam {}\n'.format(self.loc[0]))
            file.write('mv zsam {}\n'.format(self.loc[1]))
            if self.capscan_y:
                file.write('capalign ysam {} {}\n'.format(self.capscan_y[0], self.capscan_y[1]))

            if self.capscan_z:
                file.write('capalign zsam {} {}\n'.format(self.capscan_z[0], self.capscan_z[1]))


            #align
            for config, time in self.configs.items():
                file.write('current_config = {}\n'.format(config))
                file.write('conf_ugo current_config\n')

                if self.align_beamstop:
                    file.write('mv_blankpos\n')
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
        return [-8. * pos[1] + 48., 8. * pos[0] - 24]

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
