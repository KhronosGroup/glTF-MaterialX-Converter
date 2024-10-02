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

class MtlxDocumentCompare():
    '''
    @brief Class to compare two MaterialX documents.
    '''
    def __init__(self, doc1, doc2):
        '''
        @brief Constructor.
        @param doc1: The first document to compare.
        @param doc2: The second document to compare.
        '''
        self.doc1 = doc1
        self.doc2 = doc2
        self.error = ''

    def getError(self):
        '''
        @brief Get the error message.
        @return: The error message.
        '''
        return self.error

    def normalizeValueString(self, string, value_type):
        '''
        @brief Normalize a value string.
        @param string: The string to normalize.
        @param value_type: The type of the value.
        @return: The normalized string.
        '''
        supported_types = {"integer", "float", "vector2", "vector3", "vector4", "color3", "color4", "matrix33", "matrix44"}
        
        if value_type not in supported_types:
            return string
        
        token_separator = ", "
        result = ""
        
        is_integer = (value_type == "integer")
        
        if is_integer:
            # Remove leading and trailing spaces
            result = string.strip()
        else:
            tokens = string.split(',')
            for token in tokens:
                # Remove leading and trailing spaces
                token = token.strip()
                
                # Skip if the token is empty
                if not token:
                    continue
                
                # Remove leading zeros
                token = token.lstrip('0')
                
                # Preserve 0 values
                if token == "" or token[0] == '.':
                    token = "0" + token
                
                # Check if token has 'e' character for scientific notation
                if 'e' not in token:
                    # If token has a decimal point, remove trailing zeros
                    if '.' in token:
                        token = token.rstrip('0')
                        # If token ends with '.', remove it
                        if token[-1] == '.':
                            token = token[:-1]
                
                # Append the formatted token to result with separator
                result += token + token_separator
            
            # Remove the last separator
            if result:
                result = result[:-len(token_separator)]
        
        return result

    def normalizeValueStrings(self, doc):
        '''
        @brief Normalize all value strings in a document.
        @param doc: The document to normalize.
        '''
        for elem in doc.traverseTree():
            if not elem.isA(mx.ValueElement):
                continue

            original_string = elem.getValueString()
            if not original_string:
                continue

            normalized_string = self.normalizeValueString(original_string, elem.getType())
            if normalized_string != original_string:
                elem.setValueString(normalized_string)        

    def functionallyEquivalent(self, lhs, rhs):
        '''
        @brief Check if two MaterialX elements are functionally equivalent.
        @param lhs: The first element.
        @param rhs: The second element.
        @return: True if the elements are functionally equivalent, otherwise False.'''

        if lhs.getCategory() != rhs.getCategory():
            self.error = "Mismatched category: " + lhs.getName() + " vs " + rhs.getName()
            return False

        if lhs.getName() != rhs.getName():
            self.error = "Mismatched name: " + lhs.getName() + " vs " + rhs.getName()
            return False  

        # Compare attributes.
        if (len(lhs.getAttributeNames()) != len(rhs.getAttributeNames())): 
            self.error = "Mismatched number of attributes: " , len(lhs.getAttributeNames()) , " vs " , len(rhs.getAttributeNames())
            return False
        
        lhsAttrNames = lhs.getAttributeNames()
        rhsAttrNames = rhs.getAttributeNames()
        lhsAttrNames.sort()
        rhsAttrNames.sort()
        if (lhsAttrNames != rhsAttrNames):
            self.error = "Mismatched attribute names"
            return False
        
        for attr in lhsAttrNames:
            if lhs.getAttribute(attr) != rhs.getAttribute(attr):
                self.error = "Mismatched attribute: " + lhs.getAttribute(attr) + " vs " + rhs.getAttribute(attr)
                return False

        # Compare children.
        c1 = lhs.getChildren()
        c2 = rhs.getChildren()
        if len(c1) != len(c2):
            self.error = "Mismatched number of children: " , len(c1) , " vs " , len(c2)
            return False
        
        # Compare children names
        c1names = []
        for child in c1:
            c1names.append(child.getName())
        c2names = []
        for child in c2:
            c2names.append(child.getName())
        c1names.sort()
        c2names.sort()
        if c1names != c2names:
            self.error = "Mismatched children names"
            return False

        for child in c1:

            child2 = rhs.getChild(child.getName())

            #if (child2 is None):
            #    print("Missing child: " + child.getName())
            #    return False
        
            if not self.functionallyEquivalent(child, child2): 
                return False
        
        return True

    def compare(self):
        '''
        @brief Compare two MaterialX documents.
        @return: True if the documents are functionally equivalent, otherwise False.
        '''
        self.result = self.functionallyEquivalent(self.doc1, self.doc2)
        return self.result

    def normalize(self):
        '''
        @brief Normalize two MaterialX documents.
        '''
        self.normalizeValueStrings(self.doc1)
        self.normalizeValueStrings(self.doc2)

class MTlxShadingModelTranslator():
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
