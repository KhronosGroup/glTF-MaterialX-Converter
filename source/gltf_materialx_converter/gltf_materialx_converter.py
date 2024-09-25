import os, argparse
import json
import MaterialX as mx
import logging as lg 
import converter as MxGLTFPT

def main():
    parser = argparse.ArgumentParser(description="Bi-directioanl converter between MaterialX and glTF Texture Procedurals.")
    parser.add_argument(dest="input", help="Input file/folder.")
    parser.add_argument("-o", "--output", help="Output file/folder. Default is current folder.")
    parser.add_argument("-s", "--sourceType", default='.mtlx', help="Source type. Default is 'mtlx'.")
    opts = parser.parse_args()
    
    logger = lg.getLogger('gltfCmd')
    lg.basicConfig(level=lg.INFO)  

    fileList = []
    extension = ''
    if os.path.isdir(opts.input): 
        # TODO: Expand to accept glTF as input
        if opts.sourceType not in ['.mtlx']:
            logger.error(f'Invalid source type: {opts.sourceType}. Must be either mtlx or gltf.')
            return
        extension = opts.sourceType 
        fileList = MxGLTFPT.getFiles(opts.input, extension)
    else:
        extension = os.path.splitext(opts.input)[1]
        # TODO: Expand to accept glTF as input
        if extension not in ['.mtlx']:
            logger.error(f'Invalid file extension: {extension}. Must be either .mtlx or .gltf.')
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

    if extension == '.mtlx':

        for inputFile in fileList:
            logger.info(f'Processing: {inputFile}')
            mxdoc = MxGLTFPT.createWorkingDocument([stdlib])      
            MxGLTFPT.readMaterialXDocument(mxdoc, inputFile)
            valid, errors = MxGLTFPT.validateDocument(mxdoc)

            if not valid:
                logger.error(f'MaterialX document: {inputFile} is invalid. Erors: {errors}')
                continue

            if (mxdoc and mxdoc.validate()):
                jsonString, status = converter.materialXtoGLTF(mxdoc)
                if jsonString:
                    # Write string to file x.json
                    outputFile = os.path.join(outputFolder, os.path.basename(inputFile).replace('.mtlx', '.gltf'))
                    with open(outputFile, 'w') as f:
                        logger.info(f'Writing glTF: {outputFile}')
                        f.write(jsonString)

                else:
                    logger.error(f'Error: {status}')

if __name__ == '__main__':
    main()