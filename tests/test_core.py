# tests/test_core.py
# Run from root:
#   python -m unittest tests.test_core

import unittest, os, sys
import MaterialX as mx

import json
import jsonschema
from jsonschema import validate as json_validate

# Add the src directory to the sys.path
from gltf_materialx_converter import converter as MxGLTFPT
from gltf_materialx_converter import utilities as MxGLTFPTUtil

import importlib.util

def have_version(major, minor, patch):
    '''
    Check if the current vesion matches a given version
    @parm major: The major version number
    @parm minor: The minor version number
    @parm patch: The patch version number
    @return: True if the current version is greater or equal to the given version
    ''' 
    imajor, iminor, ipatch = mx.getVersionIntegers()
    print(f'Checking MaterialX version: {imajor}.{iminor}.{ipatch}')

    if major >= imajor:
        if  major > imajor:
            return True        
        if iminor >= minor:
            if iminor > minor:
                return True 
            if  ipatch >= patch:
                return True
    return False

def get_materialX_document(test_case, input_file):
    '''
    Read in a MaterialX document from a file
    @param test_case: The test case
    @param input_file: The input file
    @return: The MaterialX document
    '''
    stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()
    test_case.assertIsNotNone(stdlib)

    if not os.path.exists(input_file):
        test_case.fail(f"File not found: {input_file}")
    mxdoc = MxGLTFPTUtil.create_working_document([stdlib])      
    test_case.assertIsNotNone(stdlib)        
    mx.readFromXmlFile(mxdoc, input_file)
    valid, errors = MxGLTFPTUtil.validate_document(mxdoc)
    if not valid:
        print('> Validation failed for file:', input_file)
        print('> ' + errors)
    test_case.assertTrue(valid)
    return mxdoc


class TestConvertFromMtlx(unittest.TestCase):
    # Test conversion from MaterialX to GLTF Procedural Texture
    def test_convert_from_mtlx(self):

        if not have_version(1, 39, 0):
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

        # Read in schame file
        schema_file = os.path.join(current_folder, 'schema', 'schema.json')
        schema = None
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                schema = json.load(f)
        print('Schema file:', schema_file,)

        # Test each file
        for file, file_name in zip(test_files, test_file_names):
            
            input_file = file
            print('\n> Input test file:', file_name)

            mxdoc = get_materialX_document(self, input_file)

            # Convert from MaterialX to GLTF
            json_string, status = converter.materialX_to_glTF(mxdoc)
            self.assertTrue(len(json_string) > 0)

            # Test JSON string vs schema
            validJSON = False
            if schema:
                json_data = json.loads(json_string)  # Parse json_string to a dictionary  
                try:
                    json_validate(instance=json_data, schema=schema)  # Validate JSON data against the schema
                    print('> JSON validation successful for:', file_name.replace('.mtlx', '.gltf'))
                    validJSON = True
                except jsonschema.exceptions.ValidationError as e:
                    print('> JSON validation error for:', file_name.replace('.mtlx', '.gltf'))
                    print(e)                
            self.assertTrue(validJSON)

            # Write to disk
            gltf_name = input_file.replace('.mtlx', '.gltf')
            with open(gltf_name, 'w') as f:
                print('> Writing converted glTF file:', gltf_name)
                f.write(json_string)

class TestConvertToMtlx(unittest.TestCase):
    # Test conversion from GLTF Procedural Texture to MaterialX
    def test_convert_to_mtlx(self):

        if not have_version(1, 39, 0):
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
            # To be updated when the conversion from GLTF to MaterialX is implemented
            print('\n> Input test file:', file_name)  

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()