# tests/test_core.py
# Run from root:
#   python -m unittest tests.test_core

import unittest
import os
import logging as lg 
import MaterialX as mx

import json
import jsonschema
from jsonschema import validate as json_validate

# Add the src directory to the sys.path
from gltf_materialx_converter import converter as MxGLTFPT
from gltf_materialx_converter import utilities as MxGLTFPTUtil

import importlib.util

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

def getGLTFDocument(testCase, inputFile):
    if not os.path.exists(inputFile):
        testCase.fail(f"File not found: {inputFile}")
    jsonString = MxGLTFPTUtil.load_json_file(inputFile)
    testCase.assertIsNotNone(jsonString)
    return jsonString

class TestConvertFromMtlx(unittest.TestCase):
    '''
    Test conversion from MaterialX to GLTF Procedural Texture
    '''
    def test_convert_from_mtlx(self):

        if not MxGLTFPTUtil.have_version(1, 39, 1):
            print("MaterialX version 1.39.1 or higher is required for this test.")
            return

        logger = lg.getLogger('test')
        lg.basicConfig(level=lg.INFO)  

        have_version_1392 = MxGLTFPTUtil.have_version(1, 39,2) 
        logger.info(f'Checking MaterialX version: 1.39.2 or higher: {have_version_1392}')

        current_folder = os.path.dirname(__file__)

        # Get all files in the data folder
        test_files = []
        test_file_names = []
        for root, dirs, files in os.walk(os.path.join(current_folder, 'data')):
            for file in files:
                if file.endswith(".mtlx") and not file.endswith("_fromgltf.mtlx"):
                    test_file_names.append(file)
                    # Get absolute path
                    file = os.path.abspath(os.path.join(root, file))
                    #logger.info(f'Found test file: {file}')
                    test_files.append(file)

        # The shaders are not translated over for these intentionally
        # As one shader is not a glTF PBR shader and the other has no shader. 
        skip_diff = ['unsupported_stdsurf.mtlx', 'no_material.mtlx']

        converter = MxGLTFPT.glTFMaterialXConverter()

        # Read in schame file
        schema_file = os.path.join(current_folder, 'schema', 'schema.json')
        schema = None
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                schema = json.load(f)
        logger.info(f'Schema file: {schema_file}')

        # Test each file
        for file, file_name in zip(test_files, test_file_names):
            
            input_file = file
            logger.info('')
            logger.info(f'-------- Input MTLX file: {file_name} -------- ')  

            mxdoc = get_materialX_document(self, input_file)

            # Convert from MaterialX to GLTF
            json_string, status = converter.materialX_to_glTF(mxdoc)

            orig_doc = mx.createDocument()
            mx.readFromXmlFile(orig_doc, input_file)

            if len(json_string) > 0:
                logger.info(f'> Conversion successful for: {file_name}')
            else:
                graphs = orig_doc.getNodeGraphs()
                if len(graphs) == 0:
                    logger.info(f'> No graphs converted successfully for: {file_name}')
                else:
                    logger.info(f'> Conversion failed for: {file_name}. Status: {status}')
                continue

            # Test JSON string vs schema
            valid_json = False
            if schema:
                json_data = json.loads(json_string)  # Parse json_string to a dictionary  
                try:
                    json_validate(instance=json_data, schema=schema)  # Validate JSON data against the schema
                    logger.info('> JSON validation successful for: ' + file_name.replace('.mtlx', '.gltf'))
                    valid_json = True
                except jsonschema.exceptions.ValidationError as e:
                    logger.info('> JSON validation error for: ' + file_name.replace('.mtlx', '.gltf'))
                    logger.info(e)                
            self.assertTrue(valid_json)

            # Write to disk
            gltf_name = input_file.replace('.mtlx', '.gltf')
            with open(gltf_name, 'w') as f:
                logger.info(f'> Writing converted glTF file: {gltf_name}')
                f.write(json_string)

            if file_name in skip_diff:
                logger.info(f'> Skipping comparison for: {file_name}')
            else:
                errors = ''
                if have_version_1392:

                    # Convert back to MaterialX
                    stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()
                    self.assertIsNotNone(stdlib)
                    compare_doc = converter.gltf_string_to_materialX(json_string, stdlib)
                    self.assertIsNotNone(compare_doc)

                    # Remove material nodes as they are generated from glTF
                    for mnode in orig_doc.getMaterialNodes():
                        orig_doc.removeNode(mnode.getName())
                    for mnode in compare_doc.getMaterialNodes():
                        compare_doc.removeNode(mnode.getName())

                    # Flatten filenames for comparison
                    mx.flattenFilenames(orig_doc)

                    # Remove any comments for comparison
                    MxGLTFPTUtil.remove_comments(orig_doc)
                    MxGLTFPTUtil.remove_comments(compare_doc)

                    equivalence_opts = mx.ElementEquivalenceOptions()
                    # Always skip doc strings
                    equivalence_opts.skipAttributes = { 'doc' } 

                    equivalent, errors = orig_doc.isEquivalent(compare_doc, equivalence_opts)

                    if (not equivalent):                    
                        mx.writeToXmlFile(orig_doc, 'orig.mtlx')
                        mx.writeToXmlFile(compare_doc, 'compare.mtlx')
                        logger.info(f'> Comparison failed for file: {input_file}. Error: {errors}')
                        self.assertTrue(equivalent)
                    else:
                        logger.info(f'> Comparison passed for file: {input_file}')

class TestConvertToMtlx(unittest.TestCase):
    '''
    Test conversion from GLTF Procedural Texture to MaterialX
    '''
    def test_convert_to_mtlx(self):

        if not MxGLTFPTUtil.have_version(1, 39, 1):
            logger.error("MaterialX version 1.39.1 or higher is required for this test.")
            return

        logger = lg.getLogger('test')
        lg.basicConfig(level=lg.INFO)

        current_folder = os.path.dirname(__file__)

        # The shaders are not translated over for these intentionally
        # unsupported_stdsurf.gltf : has a non-glTF shader 
        # no_material.gltf : has no materials 
        skip_diff = ['unsupported_stdsurf.gltf', 'no_material.gltf' ]

        # Get all files in the data folder
        test_files = []
        test_file_names = []
        for root, dirs, files in os.walk(os.path.join(current_folder, 'data')):
            for file in files:
                if file.endswith(".gltf"):
                    test_file_names.append(file)
                    # Get absolute path
                    file = os.path.abspath(os.path.join(root, file))
                    #logger.info(f'Found test file: {file}')
                    test_files.append(file)

        converter = MxGLTFPT.glTFMaterialXConverter()
        converter.set_add_asset_info(True)

        for file, file_name in zip(test_files, test_file_names):

            logger.info('')
            logger.info(f'-------- Input GLTF file: {file_name} -------- ')  

            inputFile = file
            jsonString = getGLTFDocument(self, inputFile)
            self.assertIsNotNone(jsonString)

            stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()
            self.assertIsNotNone(stdlib)

            # Convert from GLTF to MaterialX
            mxdoc = converter.gltf_string_to_materialX(jsonString, stdlib)
            #logger.info('-----------------------\n' + mx.prettyPrint(mxdoc))
            mtlxFileName = inputFile.replace('.gltf', '_fromgltf.mtlx')
            logger.info("> Writing converted MaterialX file: " + file.replace('.gltf', '_fromgltf.mtlx'))
            mx.writeToXmlFile(mxdoc, mtlxFileName)

            MxGLTFPTUtil.import_libraries(mxdoc, stdlib)
            valid, status = MxGLTFPTUtil.validate_document(mxdoc)
            if not valid:
                logger.info(f'> Validation failed for file: {inputFile}')
                logger.info(status)
            self.assertTrue(valid)

            if file_name in skip_diff:
                logger.info(f'> Skipping comparison for: {file_name}')
            else:
                # Convert back to GLTF
                jsonString2, status = converter.materialX_to_glTF(mxdoc)
                json1 = json.loads(jsonString)
                converter.glTF_graph_clear_names(json1)
                json2 = json.loads(jsonString2)                
                converter.glTF_graph_clear_names(json2)
                jsonString = json.dumps(json1, sort_keys=True, indent=4)
                jsonString2 = json.dumps(json2, sort_keys=True, indent=4)
                logger.info(f'> JSON comparison match: {jsonString == jsonString2}')
                self.assertTrue(len(jsonString2) > 0)
                if (jsonString != jsonString2):
                    logger.info(f'> JSON comparison failed for file: {inputFile}')
                    with open('orig.gltf', 'w') as f:
                        f.write(jsonString) 
                    with open('compare.gltf', 'w') as f:
                        f.write(jsonString2)
                self.assertTrue(jsonString == jsonString2)

if __name__ == '__main__':
    unittest.main()