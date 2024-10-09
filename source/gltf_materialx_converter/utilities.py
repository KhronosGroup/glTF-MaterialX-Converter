# core.py

'''
@file utilities.py
This module contains the utilities for MaterialX glTF Procedural Texture graph conversion.
'''
import os
import json
import MaterialX as mx
import logging as lg 

def load_json_file(filename):
    '''Load a JSON file.
    @param filename: The file to load.
    @return: The JSON string
    '''
    json_string = ''
    with open(filename, 'r') as file:
        file = json.load(file)
        json_string = json.dumps(file, indent=2)
    return json_string    

def load_standard_libraries():
    '''Load standard MaierialX libraries.
    @return: The standard library and the list of library files.
    '''
    stdlib = mx.createDocument()
    libFiles = mx.loadLibraries(mx.getDefaultDataLibraryFolders(), mx.getDefaultDataSearchPath(), stdlib)
    return stdlib, libFiles

def create_working_document(libraries):
    '''Create a working document and import any libraries
    @param libraries: The list of definition libraries to import.
    @return: The new working document
    '''
    doc = mx.createDocument()
    for lib in libraries:
        doc.importLibrary(lib)

    return doc

def import_libraries(doc, libraries):
    '''Import libraries into a document.
    @param doc: The document to import into.
    @param libraries: The list of libraries to import.
    '''
    doc.importLibrary(libraries)

def read_materialX_document(materialx_doc, input_file):
    '''
    Read a MaterialX document from a file.
    @param materialx_doc: The MaterialX document to read into.
    @param input_file: The file to read from.
    '''
    mx.readFromXmlFile(materialx_doc, input_file)

def materialX_doc_to_string(materialx_doc):
    '''Convert a MaterialX document to a string.
    @param materialx_doc: The document to convert.
    @return: The document as a string.
    '''
    return mx.writeToXmlString(materialx_doc)

def validate_document(doc):
    '''Validate a MaterialX document.
    @param doc: The document to validate.
    @return: The validation result as a tuple of [valid, error string].
    '''
    valid, error_string = doc.validate()
    return valid, error_string

def get_files(rootPath, extension):
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

def have_version(major, minor, patch):
    '''
    Check if the current vesion matches a given version
    @parm major: The major version number
    @parm minor: The minor version number
    @parm patch: The patch version number
    @return: True if the current version is greater or equal to the given version
    ''' 
    imajor, iminor, ipatch = mx.getVersionIntegers()
    #print(f'Checking MaterialX version: {imajor}.{iminor}.{ipatch}')

    if major >= imajor:
        if  major > imajor:
            return True        
        if iminor >= minor:
            if iminor > minor:
                return True 
            if  ipatch >= patch:
                return True
    return False    


