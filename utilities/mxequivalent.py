import argparse
import sys, os
import logging as lg

import MaterialX as mx

def main():
    '''
    Perform functional equivalence testing on two MaterialX documents.
    '''
    parser = argparse.ArgumentParser(description="Test if two documents are functionally equivalent.")
    parser.add_argument(dest="inputFilename", help="Filename of the input document.")
    parser.add_argument(dest="inputFilename2", help="Filename of the input document to compare against.")
    parser.add_argument('-sa', '--skipAttributes', nargs='+', help="List of attributes to exclude from comparisons.")
    parser.add_argument('-sv', '--skipValueComparisons', action='store_true', help="Skip value comparisons. Default is False.")    
    parser.add_argument('-m', '--ignoreMaterials', action='store_true', help="Ignore materials in the comparison. Default is False.")
    parser.add_argument('-f', '--flattentFileNames', action='store_true', help="Flatten file names in the comparison. Default is False.")
    parser.add_argument('-p', '--precision', type=int, default=None, help="Specify the precision for floating-point comparisons.", )

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
        logger.error(f"File {(opts.inputFilename)} does not exist.")
        sys.exit(0)
    if not os.path.isfile(opts.inputFilename2):
        logger.error(f"File {(opts.inputFilename2)} does not exist.")
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
    if opts.skipAttributes:
        for attr in opts.skipAttributes:
            equivalence_opts.skipAttributes.add(attr)
    if opts.skipValueComparisons:
        equivalence_opts.skipValueComparisons = True
    if opts.precision:
        equivalence_opts.precision = opts.precision

    # Always skip doc strings
    equivalence_opts.skipAttributes = { 'doc' }

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

    equivalent, results = doc.isEquivalent(doc2, equivalence_opts)
    if equivalent:
        logger.info(f"Documents are equivalent: {opts.inputFilename} and {opts.inputFilename2}")
    else:
        print(results)
        logger.info(f"Documents are not equivalent: {len(results)} differences found")
        for i in range(0, len(results)):
            difference = results[i]
            logger.info(f"  - Difference[{i}] : Path: '{difference.path1}' vs path: '{difference.path2}'. Difference Type: '{difference.differenceType}'"
                  + (f". Attribute: '{difference.attributeName}'" if difference.attributeName else "")) 
            sys.exit(-1)
    
if __name__ == '__main__':
    main()

