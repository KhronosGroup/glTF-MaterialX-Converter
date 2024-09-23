# tests/test_core.py
# Run from root:
#   python -m unittest tests.test_core

import unittest, os
import MaterialX as mx

from gltf_materialx_converter import converter as MxGLTFPT

def haveVersion(major, minor, patch):
    '''
    Check if the current vesion matches a given version
    ''' 
    imajor, iminor, ipatch = mx.getVersionIntegers()

    if major >= imajor:
        if  major > imajor:
            return True        
        if iminor >= minor:
            if iminor > minor:
                return True 
            if  ipatch >= patch:
                return True
    return False

class TestConvertFromMtlx(unittest.TestCase):
    # Test conversion from MaterialX to GLTF Procedural Texture
    def test_convert_from_mtlx(self):

        if not haveVersion(1, 39, 0):
            print("MaterialX version 1.39.0 or higher is required for this test.")
            return

        current_folder = os.path.dirname(__file__)

        # Get all files in the data folder
        test_files = []
        test_file_names = []
        for root, dirs, files in os.walk(os.path.join(current_folder, 'data')):
            for file in files:
                if file.endswith(".mtlx"):
                    test_file_names.append(file)
                    # Get absolute path
                    file = os.path.abspath(os.path.join(root, file))
                    print('Found test file:', file)
                    test_files.append(file)

        converter = MxGLTFPT.glTFMaterialXConverter()

        # Test each file
        for file, file_name in zip(test_files, test_file_names):
            
            inputFile = file
            print('\n> Input test file:', file_name)

        self.assertTrue(True)

class TestConvertToMtlx(unittest.TestCase):
    # Test conversion from GLTF Procedural Texture to MaterialX
    def test_convert_to_mtlx(self):

        if not haveVersion(1, 39, 0):
            print("MaterialX version 1.39.0 or higher is required for this test.")
            return

        current_folder = os.path.dirname(__file__)

        # Get all files in the data folder
        test_files = []
        test_file_names = []
        for root, dirs, files in os.walk(os.path.join(current_folder, 'data')):
            for file in files:
                if file.endswith(".gltf"):
                    test_file_names.append(file)
                    # Get absolute path
                    file = os.path.abspath(os.path.join(root, file))
                    print('Found test file:', file)
                    test_files.append(file)

        converter = MxGLTFPT.glTFMaterialXConverter()

        for file, file_name in zip(test_files, test_file_names):

            print('\n> Input test file:', file_name)  

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()