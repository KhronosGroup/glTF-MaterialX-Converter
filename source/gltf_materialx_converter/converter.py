# converter.py

'''
@file converter.py
This module contains the core functionality for MaterialX glTF ProceduralTexture graph conversion.
'''
import MaterialX as mx
import logging as lg 

class glTFMaterialXConverter():
    """
    @brief Class for converting to convert between glTF Texture Procedurals content and MaterialX
    """

    def __init__(self):
        """
        Constructor

        **Attributes**
        - logger : logging.Logger
            - Logger instance for the class, used to log information, warnings, and errors.

        """
        super().__init__()

        self.logger = lg.getLogger('glTFMtlx')
        lg.basicConfig(level=lg.INFO)  

    def set_debug(self, debug):
        """
        Set the debug flag for the converter.
        @param debug: The debug flag.
        """
        if debug:
            self.logger.setLevel(lg.DEBUG)
        else:
            self.logger.setLevel(lg.INFO)
    

    
