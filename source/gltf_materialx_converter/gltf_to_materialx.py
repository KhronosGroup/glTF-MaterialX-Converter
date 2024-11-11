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
    parser.add_argument("-c", "--addComments", type=bool, default=False, help="Add comments to generated MaterialX files.")
    parser.add_argument("-nd", "--addNodeDefStrings" , type=bool, default=False, help="Add nodeDef strings to generated MaterialX files.")
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
            logger.error(f'Invalid file extension: {extension}. Must be either .gltf.')
            return
        fileList.append(opts.input)

    if not fileList:
        logger.info(f'No glTF content to process: {opts.input}')
        return
    
    stdlib, libFiles = MxGLTFPTUtil.load_standard_libraries()

    converter = MxGLTFPT.glTFMaterialXConverter()

    # Check for output folder option
    outputFolder = '.'
    if opts.output:
        outputFolder = opts.output
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    print('add comments:', opts.addComments, "add node def strings:", opts.addNodeDefStrings)
    converter.set_add_xml_comments(opts.addComments)
    converter.set_add_nodedef_strings(opts.addNodeDefStrings)

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
            logger.error(f'Unable to load glTF file: {inputFile}')

if __name__ == '__main__':
    main()