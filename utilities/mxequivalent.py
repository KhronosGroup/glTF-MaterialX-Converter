# @file mxequivalent
# @brief Sample wrapper script to test if two documents are functionally equivalent.
#
import argparse
import sys
import os
import logging as lg

import MaterialX as mx

def main():
    # Sample wrapper script to test if two documents are functionally equivalent.
    # Uses the MaterialX Python API to read two documents from file and compare them.
    # The comparison can be customized by specifying a list of attributes to exclude from comparisons,
    # skipping value comparisons, ignoring materials, flattening file names, and specifying the precision for floating-point comparisons.
    # The script logs the results of the comparison to the console.
    parser = argparse.ArgumentParser(description='Test if two documents are functionally equivalent.')
    parser.add_argument(dest='inputFilename', help='Filename of the input document.')
    parser.add_argument(dest='inputFilename2', help='Filename of the input document to compare against.')
    parser.add_argument('-sa', '--attributeExclusionList', nargs='+', help='List of attributes to exclude from comparisons.')
    parser.add_argument('-sv', '--skipValueComparisons', action='store_true', help='Skip value comparisons. Default is False.')    
    parser.add_argument('-m', '--ignoreMaterials', action='store_true', help='Ignore materials in the comparison. Default is False.')
    parser.add_argument('-f', '--flattentFileNames', action='store_true', help='Flatten file names in the comparison. Default is False.')
    parser.add_argument('-p', '--precision', type=int, default=None, help='Specify the precision for floating-point comparisons.', )

    opts = parser.parse_args()

    logger = lg.getLogger('mxequivalent')
    lg.basicConfig(level=lg.INFO)  
    logResults = False
    if logResults:
        fh = lg.FileHandler('mxequivalent.log')
        fh.setLevel(lg.INFO)
        logger.addHandler(fh)

    # Check if both files exist
    if not os.path.isfile(opts.inputFilename):
        logger.error(f'File {(opts.inputFilename)} does not exist.')
        sys.exit(0)
    if not os.path.isfile(opts.inputFilename2):
        logger.error(f'File {(opts.inputFilename2)} does not exist.')
        sys.exit(0)

    doc = mx.createDocument()
    try:
        mx.readFromXmlFile(doc, opts.inputFilename)
    except mx.ExceptionFileMissing as err:
        logger.error(err)
        sys.exit(0)

    doc2 = mx.createDocument()
    try:
        mx.readFromXmlFile(doc2, opts.inputFilename2)
    except mx.ExceptionFileMissing as err:
        logger.error(err)
        sys.exit(0)

    major, minor, patch = mx.getVersionIntegers()
    if major < 1:
        logger.error(f'Unsupport version: {mx.getVersionString()}')
        return
    elif minor < 30:
        logger.error(f'Unsupport version: {mx.getVersionString()}')
        return
    elif patch < 2:
        logger.error(f'Unsupport version: {mx.getVersionString()}')
        return
    else:
        logger.info(f'Have supported version: {mx.getVersionString()}')

    equivalence_opts = mx.ElementEquivalenceOptions()
    if opts.attributeExclusionList:
        for attr in opts.attributeExclusionList:
            equivalence_opts.attributeExclusionList.add(attr)
    if opts.skipValueComparisons:
        equivalence_opts.performValueComparisons = False
    if opts.precision:
        equivalence_opts.precision = opts.precision

    # Always skip doc strings
    equivalence_opts.attributeExclusionList = { 'doc' }

    # Remove material nodes if requested
    if opts.ignoreMaterials:
        logger.info('Remove material nodes before comparison')
        for mnode in doc.getMaterialNodes():
            doc.removeNode(mnode.getName())
        for mnode in doc2.getMaterialNodes():
            doc2.removeNode(mnode.getName())

    # Flatten file names if requested
    if opts.flattentFileNames:
        logger.info('Flattening file names before comparison')
        mx.flattenFilenames(doc)
        mx.flattenFilenames(doc2)

    equivalent, message = doc.isEquivalent(doc2, equivalence_opts)
    if equivalent:
        logger.info(f'Documents are equivalent: {opts.inputFilename} and {opts.inputFilename2}')
    else:
        logger.info(f'Documents are not equivalent: "{message}"')
        sys.exit(-1)
    
if __name__ == '__main__':
    main()

