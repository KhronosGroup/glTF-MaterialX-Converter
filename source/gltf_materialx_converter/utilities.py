# core.py

'''
@file utilities.py
This module contains the utilities for MaterialX glTF Procedural Texture graph conversion.
'''
import os
import json
import MaterialX as mx
import logging as lg 

def loadJsonFile(filename):
    '''Load a JSON file.
    @param filename: The file to load.
    @return: The JSON string
    '''
    jsonString = ''
    with open(filename, 'r') as file:
        file = json.load(file)
        jsonString = json.dumps(file, indent=2)
    return jsonString    

def loadStandardLibraries():
    '''Load standard MaierialX libraries.
    @return: The standard library and the list of library files.
    '''
    stdlib = mx.createDocument()
    libFiles = mx.loadLibraries(mx.getDefaultDataLibraryFolders(), mx.getDefaultDataSearchPath(), stdlib)
    return stdlib, libFiles

def createWorkingDocument(libraries):
    '''Create a working document and import any libraries
    @param libraries: The list of definition libraries to import.
    @return: The new working document
    '''
    doc = mx.createDocument()
    for lib in libraries:
        doc.importLibrary(lib)

    return doc

def importLibraries(doc, libraries):
    '''Import libraries into a document.
    @param doc: The document to import into.
    @param libraries: The list of libraries to import.
    '''
    doc.importLibrary(libraries)

def readMaterialXDocument(mtlxdoc, inputFile):
    '''
    Read a MaterialX document from a file.
    @param mtlxdoc: The MaterialX document to read into.
    @param inputFile: The file to read from.
    '''
    mx.readFromXmlFile(mtlxdoc, inputFile)

def materialXDocToString(mtlxdoc):
    '''Convert a MaterialX document to a string.
    @param mtlxdoc: The document to convert.
    @return: The document as a string.
    '''
    return mx.writeToXmlString(mtlxdoc)

def validateDocument(doc):
    '''Validate a MaterialX document.
    @param doc: The document to validate.
    @return: The validation result as a tuple of [valid, errorString].
    '''
    valid, errorString = doc.validate()
    return valid, errorString

def getFiles(rootPath, extension):
    '''Get all files with a given extension in a directory.
    @param rootPath: The root directory to search.
    @param extension: The file extension to search for.
    @return: The list of files with the given extension.
    '''
    filelist = []
    exts = (extension)
    for subdir, dirs, files in os.walk(rootPath):
        for file in files:
            if file.lower().endswith(exts):
                filelist.append(os.path.join(subdir, file)) 
    return filelist

class MtlxShadingModelTranslator():
    '''
    @brief Class to translate shading models within a MaterialX document.    
    '''
    def __init__(self):
        '''
        @brief Constructor.
        '''
        pass

    def translate(self, doc, target='gltf'): 
        '''
        Translate the shading model to a target shading model 
        @param doc: The MaterialX document to translate
        @param target: The target shading model. Default is gltf
        @return: The translated document if successful, otherwise None
        '''
        translatedDoc = doc.copy()
        translator = mx.ShaderTranslator.create()

        try:
            translator.translateAllMaterials(translatedDoc, target)
            return translatedDoc
        except Exception as e:
            print(f'Translation failed to target: {target}')
            return None
