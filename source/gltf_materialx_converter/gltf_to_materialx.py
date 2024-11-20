'''
@file gltf_to_materialx.py
Command line utility to convert from glTF Texture Procedurals documents to MaterialX documents".
'''
import os, argparse
import json
import MaterialX as mx
import logging as lg 
import converter as MxGLTFPT
import utilities as MxGLTFPTUtil

def main():
    parser = argparse.ArgumentParser(description="Converter from glTF Texture Procedurals to MaterialX")
    parser.add_argument(dest="input", help="Input file/folder.")
    parser.add_argument("-o", "--output", help="Output file/folder. Default is current folder.")
    parser.add_argument("-a", "--addAssetInfo", type=bool, default=False, help="Add glTF asset information to generated MaterialX files.")
    opts = parser.parse_args()
    
    logger = lg.getLogger('gltfCmd')
    lg.basicConfig(level=lg.INFO)  

    fileList = []
    extension = '.gltf'
    if os.path.isdir(opts.input): 
        fileList = MxGLTFPTUtil.getFiles(opts.input, extension)
    else:
        extension = os.path.splitext(opts.input)[1]
        if extension not in ['.gltf']:
            logger.warning(f'Invalid file extension: {extension}. Extension must be .gltf.')
            return
        fileList.append(opts.input)

    if not fileList:
        logger.warning(f'No glTF files found: {opts.input}')
        return
    
    stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()

    converter = MxGLTFPT.glTFMaterialXConverter()

    # Check for output folder option
    outputFolder = '.'
    if opts.output:
        outputFolder = opts.output
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    logger.info(f'Add glTF asset information: {opts.addAssetInfo}')
    converter.set_add_asset_info(opts.addAssetInfo)

    for inputFile in fileList:
        logger.info(f'Processing: {inputFile}')
        jsonString = MxGLTFPTUtil.load_json_file(inputFile)
        if jsonString:
            mtlxdoc = converter.gltf_string_to_materialX(jsonString, stdlib)
            # Validate
            valid, status = MxGLTFPTUtil.validate_document(mtlxdoc)
            mtlxString = MxGLTFPTUtil.materialX_doc_to_string(mtlxdoc)
            
            if not valid:
                logger.warning(f'Created invalid MaterialX document. Error: {status}')
            outputFileMtlx = inputFile.replace('.gltf', '_fromgltf.mtlx')
            with open(outputFileMtlx, 'w') as f:
                logger.info(f'Writing re-converted mtlx: {outputFileMtlx}')
                f.write(mtlxString)
        else:
            logger.warning(f'Unable to load glTF file: {inputFile}')

if __name__ == '__main__':
    main()