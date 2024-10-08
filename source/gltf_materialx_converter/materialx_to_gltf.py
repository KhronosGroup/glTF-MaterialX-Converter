import os
import argparse
import sys
import logging as lg 

import json
import jsonschema
from jsonschema import validate as json_validate

import MaterialX as mx

import converter as MxGLTFPT
import utilities as MxGLTFPTUtil

def main():
    parser = argparse.ArgumentParser(description="Conveter from MaterialX to glTF Texture Procedurals.")
    parser.add_argument(dest="input", help="Input file/folder.")
    parser.add_argument("-o", "--output", help="Output file/folder. The default is current folder.")
    parser.add_argument('-s', '--schema', default=None, help='Schema file to use for validation. The default is None.')
    opts = parser.parse_args()
    
    logger = lg.getLogger('gltfCmd')
    lg.basicConfig(level=lg.INFO)  

    if not MxGLTFPTUtil.have_version(1, 39, 1):
        logger.error("MaterialX version 1.39.1 or higher is required.")
        sys.exit(-1)

    file_list = []
    extension = '.mtlx'
    if os.path.isdir(opts.input): 
        file_list = MxGLTFPT.get_files(opts.input, extension)
    else:
        extension = os.path.splitext(opts.input)[1]
        if extension not in ['.mtlx']:
            logger.error(f'Invalid file extension: {extension}. Must be .mtlx.')
            return
        file_list.append(opts.input)

    if not file_list:
        logger.info(f'No MaterialX files found in: {opts.input}')
        return
    
    stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()

    converter = MxGLTFPT.glTFMaterialXConverter()

    # Check for output folder option
    output_folder = '.'
    if opts.output:
        output_folder = opts.output
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check for shema file option
    schema = None
    schema_file = opts.schema
    if schema_file and os.path.exists(schema_file):
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        print('Loaded schema file:', schema_file)

    for input_file in file_list:
        logger.info(f'Processing: {input_file}')
        mxdoc = MxGLTFPTUtil.create_working_document([stdlib])    
        MxGLTFPTUtil.read_materialX_document(mxdoc, input_file)
        valid, errors = MxGLTFPTUtil.validate_document(mxdoc)

        if not valid:
            logger.error(f'MaterialX document: {input_file} is invalid. Erors: {errors}')
            continue

        # Convert to glTF JSON
        json_string, status = converter.materialX_to_glTF(mxdoc)
        if json_string:
            if schema:
                json_data = json.loads(json_string)  # Parse json_string to a dictionary  
                try:
                    json_validate(instance=json_data, schema=schema)  # Validate JSON data against the schema
                    print('- JSON validation successful')
                except jsonschema.exceptions.ValidationError as e:
                    print('- JSON validation errors, ' + e)

            # Write string to file replacing .mtlx with .json extension name
            outputFile = os.path.join(output_folder, os.path.basename(input_file).replace('.mtlx', '.gltf'))
            with open(outputFile, 'w') as f:
                logger.info(f'Writing glTF: {outputFile}')
                f.write(json_string)

        else:
            logger.error(f'Error: {status}')

if __name__ == '__main__':
    main()