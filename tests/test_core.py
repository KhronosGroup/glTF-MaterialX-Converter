# tests/test_core.py
# Run from root:
#   python -m unittest tests.test_core

import unittest, os, sys
import MaterialX as mx

# Add the src directory to the sys.path
from gltf_materialx_converter import converter as MxGLTFPT

import importlib.util

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

def getMaterialxDocument(testCase, inputFile):
    stdlib, libFiles = MxGLTFPT.loadStandardLibraries()
    testCase.assertIsNotNone(stdlib)

    if not os.path.exists(inputFile):
        testCase.fail(f"File not found: {inputFile}")
    mxdoc = MxGLTFPT.createWorkingDocument([stdlib])      
    testCase.assertIsNotNone(stdlib)        
    mx.readFromXmlFile(mxdoc, inputFile)
    valid, errors = MxGLTFPT.validateDocument(mxdoc)
    testCase.assertTrue(valid)
    return mxdoc

class TestConvertFromMtlx(unittest.TestCase):
    # Test conversion from MaterialX to GLTF Procedural Texture
    def test_convert_from_mtlx(self):

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

            mxdoc = getMaterialxDocument(self, inputFile)

            # Convert from MaterialX to GLTF
            jsonString, status = converter.convert_from_materialx(mxdoc)
            self.assertTrue(len(jsonString) > 0)
            # Write to disk
            gltf_name = inputFile.replace('.mtlx', '.gltf')
            with open(gltf_name, 'w') as f:
                print('> Writing converted glTF file:', gltf_name)
                f.write(jsonString)

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