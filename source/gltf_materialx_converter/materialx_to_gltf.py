import os, argparse
import logging as lg 

import json
import jsonschema
from jsonschema import validate as json_validate

import MaterialX as mx

import converter as MxGLTFPT

def main():
    parser = argparse.ArgumentParser(description="Conveter from MaterialX to glTF Texture Procedurals.")
    parser.add_argument(dest="input", help="Input file/folder.")
    parser.add_argument("-o", "--output", help="Output file/folder. The default is current folder.")
    parser.add_argument('-s', '--schema', default=None, help='Schema file to use for validation. The default is None.')
    opts = parser.parse_args()
    
    logger = lg.getLogger('gltfCmd')
    lg.basicConfig(level=lg.INFO)  

    fileList = []
    extension = '.mtlx'
    if os.path.isdir(opts.input): 
        fileList = MxGLTFPT.getFiles(opts.input, extension)
    else:
        extension = os.path.splitext(opts.input)[1]
        if extension not in ['.mtlx']:
            logger.error(f'Invalid file extension: {extension}. Must be .mtlx.')
            return
        fileList.append(opts.input)

    if not fileList:
        logger.info(f'No MaterialX files found in: {opts.input}')
        return
    
    stdlib, libFiles = MxGLTFPT.loadStandardLibraries()

    converter = MxGLTFPT.glTFMaterialXConverter()

    # Check for output folder option
    outputFolder = '.'
    if opts.output:
        outputFolder = opts.output
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # Check for shema file option
    schema = None
    schema_file = opts.schema
    if schema_file and os.path.exists(schema_file):
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        print('Loaded schema file:', schema_file)

    for inputFile in fileList:
        logger.info(f'Processing: {inputFile}')
        mxdoc = MxGLTFPT.createWorkingDocument([stdlib])    
        MxGLTFPT.readMaterialXDocument(mxdoc, inputFile)
        valid, errors = MxGLTFPT.validateDocument(mxdoc)

        if not valid:
            logger.error(f'MaterialX document: {inputFile} is invalid. Erors: {errors}')
            continue

        # Convert to glTF JSON
        jsonString, status = converter.materialXtoGLTF(mxdoc)
        if jsonString:
            if schema:
                jsonData = json.loads(jsonString)  # Parse jsonString to a dictionary  
                try:
                    json_validate(instance=jsonData, schema=schema)  # Validate JSON data against the schema
                    print('- JSON validation successful')
                except jsonschema.exceptions.ValidationError as e:
                    print('- JSON validation errors, ' + e)

            # Write string to file replacing .mtlx with .json extension name
            outputFile = os.path.join(outputFolder, os.path.basename(inputFile).replace('.mtlx', '.gltf'))
            with open(outputFile, 'w') as f:
                logger.info(f'Writing glTF: {outputFile}')
                f.write(jsonString)

        else:
            logger.error(f'Error: {status}')

if __name__ == '__main__':
    main()