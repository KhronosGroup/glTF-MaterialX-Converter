# converter.py

'''
@file converter.py
This module contains the core functionality for MaterialX glTF ProceduralTexture graph conversion.
'''
import os, argparse
import json
import MaterialX as mx
import logging as lg 

## @var MTLX_GLTF_PBR_CATEGORY
#  @brief Category string for glTF PBR shading model in MaterialX.
MTLX_GLTF_PBR_CATEGORY = 'gltf_pbr'

## @var MTLX_INTERFACEINPUT_NAME_ATTRIBUTE
#  @brief Attribute for interface references in MaterialX.
MTLX_INTERFACEINPUT_NAME_ATTRIBUTE = 'interfacename'

## @var MTLX_NODE_NAME_ATTRIBUTE
#  @brief Attribute for node references in MaterialX.
MTLX_NODE_NAME_ATTRIBUTE = 'nodename'

## @var MTLX_NODEGRAPH_NAME_ATTRIBUTE
#  @brief Attribute for nodegraph references in MaterialX.
MTLX_NODEGRAPH_NAME_ATTRIBUTE = 'nodegraph'

class glTFMaterialXConverter():
    """
    @brief Class for converting to convert between glTF Texture Procedurals content and MaterialX
    """

    def __init__(self):
        """
        Constructor

        **Attributes**
        - logger : logging.Logger
            - Logger instance for the class, used to log information, warnings, and errors.

        - add_comments : bool
            - Option to add comments during the conversion to MaterialX.
        
        - add_nodedef_strings : bool
            - Option to add node definition strings during the conversion to MaterialX.
        
        - supported_types : list of str
            - List of supported data types for conversion.

        - array_types : list of str
            - List of supported array types for conversion.        
        """
        self.logger = lg.getLogger('glTFMtlx')
        lg.basicConfig(level=lg.INFO)  

        # Options for conversion from Materialx
        self.supported_types = ['boolean', 'string', 'integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.array_types = ['matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'color3', 'color4']

    def set_debug(self, debug):
        """
        Set the debug flag for the converter.
        @param debug: The debug flag.
        """
        if debug:
            self.logger.setLevel(lg.DEBUG)
        else:
            self.logger.setLevel(lg.INFO)
    
    def string_to_scalar(self, value, type):
        """
        Convert a string to a scalar value.
        @param value: The string value to convert.
        @param type: The type of the value.
        @return The converted scalar value if successful, otherwise the original string value.
        """
        return_value = value
    
        scalar_types = ['integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
    
        if type in scalar_types:
            split_value = value.split(',')
    
            if len(split_value) > 1:
                return_value = list(map(float, split_value))
            else:
                if type == 'integer':
                    return_value = int(value)
                else:
                    return_value = float(value)
    
        return return_value

    def materialx_graph_to_gltf(self, graph, json, materials):
        """
        Export a MaterialX nodegraph to a glTF procedural graph.
        @param graph: The MaterialX nodegraph to export.
        @param json: The JSON object to export the procedural graph to.
        @param materials: The list of materials filter out to export. Default is None
        meaning to export all materials.
        @return The procedural graph JSON object if successful, otherwise None.
        """
        no_result = [None, None, None]

        graph_outputs = graph.getOutputs()
        if len(graph_outputs) == 0:
            self.logger.info('> No graph outputs found on graph:', graph.getNamePath())
            return no_result

        debug = False
        use_paths = False

        # Create fallback texture. Seperate out
        fallback = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4z/AfAAQAAf/zKSWvAAAAAElFTkSuQmCC'
        fallback_index = -1

        image_array = json.get('images', [])
        if 'images' not in json:
            json['images'] = image_array

        for i, image in enumerate(image_array):
            if image['uri'] == fallback:
                fallback_index = i
                break

        fallback_texture_index = -1
        if fallback_index == -1:
            image = {
                'uri': fallback,
                'name': 'KHR_texture_procedural_fallback'
            }
            image_array.append(image)
            fallback_index = len(image_array) - 1

        texture_array = json.get('textures', [])
        if 'textures' not in json:
            json['textures'] = texture_array

        for i, texture in enumerate(texture_array):
            if texture['source'] == fallback_index:
                fallback_texture_index = i
                break

        if fallback_texture_index == -1:
            texture_array.append({'source': fallback_index})
            fallback_texture_index = len(texture_array) - 1

        proc_dict_nodes = {}
        proc_dict_inputs = {}
        proc_dict_outputs = {}

        extensions = json.get('extensions', {})
        if 'extensions' not in json:
            json['extensions'] = extensions

        KHR_texture_procedurals = extensions.get('KHR_texture_procedurals', {})
        if 'KHR_texture_procedurals' not in extensions:
            extensions['KHR_texture_procedurals'] = KHR_texture_procedurals

        if 'procedurals' not in KHR_texture_procedurals:
            KHR_texture_procedurals['procedurals'] = []

        procs = KHR_texture_procedurals['procedurals']
        nodegraph = {
            'name': graph.getNamePath() if use_paths else graph.getName(),
            'nodetype': graph.getCategory()
        }

        nodegraph['type'] = 'multioutput' if len(graph_outputs) > 1 else graph_outputs[0].getType()
        nodegraph['inputs'] = []
        nodegraph['outputs'] = []
        nodegraph['nodes'] = []
        procs.append(nodegraph)

        metadata = ['colorspace', 'unit', 'unittype', 'uiname', 'uimin', 'uimax', 'uifolder', 'doc']

        for node in graph.getNodes():
            json_node = {'name': node.getNamePath() if use_paths else node.getName()}
            nodegraph['nodes'].append(json_node)
            proc_dict_nodes[node.getNamePath()] = len(nodegraph['nodes']) - 1

        for input in graph.getInputs():
            json_node = {
                'name': input.getNamePath() if use_paths else input.getName(),
                'nodetype': input.getCategory()
            }

            for meta in metadata:
                if input.getAttribute(meta):
                    json_node[meta] = input.getAttribute(meta)

            if input.getValue() is not None:
                input_type = input.getAttribute(mx.TypedElement.TYPE_ATTRIBUTE)
                json_node['type'] = input_type
                if input_type == mx.FILENAME_TYPE_STRING:
                    self.logger.warning('> File texture inputs not supported:', input.getNamePath())

                value = input.getValueString()
                value = self.string_to_scalar(value, input_type)
                json_node['value'] = value
                nodegraph['inputs'].append(json_node)
                proc_dict_inputs[input.getNamePath()] = len(nodegraph['inputs']) - 1
            else:
                self.logger.error('> No value or invalid connection specified for input. Input skipped:', input.getNamePath())

        for output in graph_outputs:
            json_node = {'name': output.getNamePath() if use_paths else output.getName()}
            nodegraph['outputs'].append(json_node)
            proc_dict_outputs[output.getNamePath()] = len(nodegraph['outputs']) - 1

            json_node['nodetype'] = output.getCategory()
            json_node['type'] = output.getType()

            connection = output.getAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE)
            if len(connection) == 0:
                connection = output.getAttribute(MTLX_NODE_NAME_ATTRIBUTE)

            connection_node = graph.getChild(connection)
            if connection_node:
                connection_path = connection_node.getNamePath()
                if debug:
                    json_node['debug_connection_path'] = connection_path

                if proc_dict_inputs.get(connection_path) is not None:
                    json_node['input'] = proc_dict_inputs[connection_path]
                elif proc_dict_nodes.get(connection_path) is not None:
                    json_node['node'] = proc_dict_nodes[connection_path]
                else:
                    self.logger.error(f'> Invalid output connection to: {connection_path}')

                output_string = output.getAttribute('output')
                if len(output_string) > 0:
                    json_node['output'] = output_string

        for node in graph.getNodes():
            json_node = nodegraph['nodes'][proc_dict_nodes[node.getNamePath()]]
            json_node['nodetype'] = node.getCategory()
            nodedef = node.getNodeDef()

            if debug and nodedef and nodedef.getNodeGroup():
                json_node['nodegroup'] = nodedef.getNodeGroup()

            for attr_name in node.getAttributeNames():
                json_node[attr_name] = node.getAttribute(attr_name)

            inputs = []
            for input in node.getInputs():
                input_item = {
                    'name': input.getName(),
                    'nodetype': 'input'
                }

                for meta in metadata:
                    if input.getAttribute(meta):
                        input_item[meta] = input.getAttribute(meta)

                input_type = input.getAttribute(mx.TypedElement.TYPE_ATTRIBUTE)
                input_item['type'] = input_type

                if input.getValue() is not None:
                    if input_type == mx.FILENAME_TYPE_STRING:
                        self.logger.warning('> File texture inputs not supported:', input.getNamePath())

                    value = input.getValueString()
                    value = self.string_to_scalar(value, input_type)
                    input_item['value'] = value
                else:
                    is_interface = True
                    connection = input.getAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE)
                    if not connection:
                        is_interface = False
                        connection = input.getAttribute(MTLX_NODE_NAME_ATTRIBUTE)

                    if connection:
                        connection_node = graph.getChild(connection)
                        if connection_node:
                            connection_path = connection_node.getNamePath()
                            if debug:
                                input_item['debug_connection_path'] = connection_path

                            if is_interface and proc_dict_inputs.get(connection_path) is not None:
                                input_item['input'] = proc_dict_inputs[connection_path]
                            elif proc_dict_nodes.get(connection_path) is not None:
                                input_item['node'] = proc_dict_nodes[connection_path]

                            output_string = input.getAttribute('output')
                            if output_string:
                                connected_node_outputs = connection_node.getOutputs()
                                for i, connected_output in enumerate(connected_node_outputs):
                                    if connected_output.getName() == output_string:
                                        input_item['output'] = i
                                        break
                        else:
                            self.logger.error(f'> Invalid input connection to: '
                                              '{connection} from input: {input.getNamePath()} '
                                              'node: {node.getNamePath()}')

                inputs.append(input_item)

            if inputs:
                json_node['inputs'] = inputs

            outputs = []
            for output in node.getOutputs():
                output_item = {
                    'nodetype': 'output',
                    'name': output.getName(),
                    'type': output.getType()
                }
                outputs.append(output_item)

            if nodedef:
                for output in nodedef.getOutputs():
                    if not any(output_item['name'] == output.getName() for output_item in outputs):
                        output_item = {
                            'nodetype': 'output',
                            'name': output.getName(),
                            'type': output.getType()
                        }
                        outputs.append(output_item)
            else:
                self.logger.warning(f'> Missing nodedef for node: {node.getNamePath()}')

            if outputs:
                json_node['outputs'] = outputs

        return [procs, proc_dict_outputs, proc_dict_nodes, fallback_texture_index]

    def convert_from_materialx(self, mtlxDoc):
        """
        @brief Convert to a glTF document from a MaterialX document.
        @param mtlxDoc: The MaterialX document to convert.
        @return glTF JSON string and status message.
        """

        status = ''
        if not mtlxDoc:
            status = 'Invalid document to convert'
            return None, status

        materials = []
        mxMaterials = mtlxDoc.getMaterialNodes()
        if len(mxMaterials) == 0:
            self.logger.warning('> No materials found in document')
            #return None, status # No MaterialX materials found in the document

        json_data = {}
        json_asset = {
            "version": "2.0",
            "generator": "MaterialX 1.39 / glTF 2.0 procedural texture converter",
        }

        inputMaps = {}
        # Supported input mappings
        inputMaps[MTLX_GLTF_PBR_CATEGORY] = [
            ['base_color', 'baseColorTexture', 'pbrMetallicRoughness']
        ]

        pbrNodes = {}
        fallbackTextureIndex = -1
        procs = []
        exportGraphNames = []

        extensionsUsed = ['KHR_texture_procedurals', 'EXT_texture_procedurals_mx_1_39']

        for mxMaterial in mxMaterials:
            mxshaders = mx.getShaderNodes(mxMaterial)
            for shaderNode in mxshaders:
                category = shaderNode.getCategory()
                path = shaderNode.getNamePath()
                isPBR = (category == MTLX_GLTF_PBR_CATEGORY)
                if (isPBR) and pbrNodes.get(path) is None:
                    self.logger.info(f'> Convert shader to glTF: {shaderNode.getNamePath()}. Category: {category}')
                    pbrNodes[path] = shaderNode

                    material = {}

                    material['name'] = path

                    base_color_input = None
                    base_color_output = ''
                    inputPairs = inputMaps[category]
                    for inputPair in inputPairs:
                        base_color_input = shaderNode.getInput(inputPair[0])
                        base_color_output = inputPair[1]

                        if not base_color_input:
                            continue

                        nodeGraphName = base_color_input.getNodeGraphString()
                        if len(nodeGraphName) == 0:
                            continue

                        nodeGraphOutput = base_color_input.getOutputString()

                        parent = material
                        if len(inputPair[2]) > 0:
                            if inputPair[2] not in material:
                                material[inputPair[2]] = {}
                            parent = material[inputPair[2]]

                        graphIndex = -1
                        outputIndex = -1
                        if procs:
                            for i, proc in enumerate(procs):
                                if proc['name'] == nodeGraphName:
                                    graphIndex = i
                                    if len(nodeGraphOutput) > 0:
                                        for j, output in enumerate(proc['outputs']):
                                            if output['name'] == nodeGraphOutput:
                                                outputIndex = j
                                                break
                                    break

                        if graphIndex >= 0:
                            baseColorTexture = parent[base_color_output] = {}
                            baseColorTexture['index'] = fallbackTextureIndex
                            ext = baseColorTexture['extensions'] = {}
                            lookup = ext['KHR_texture_procedurals'] = {}
                            lookup['index'] = graphIndex
                            if outputIndex >= 0:
                                lookup['output'] = outputIndex
                        else:
                            graph = mtlxDoc.getNodeGraph(nodeGraphName)
                            exportGraphNames.append(nodeGraphName)

                            gltfInfo = self.materialx_graph_to_gltf(graph, json_data, materials)
                            procs = gltfInfo[0]
                            outputNodes = gltfInfo[1]
                            fallbackTextureIndex = gltfInfo[3]

                            baseColorTexture = parent[base_color_output] = {}
                            baseColorTexture['index'] = fallbackTextureIndex
                            ext = baseColorTexture['extensions'] = {}
                            lookup = ext['KHR_texture_procedurals'] = {}
                            lookup['index'] = len(procs) - 1
                            outputIndex = -1

                            if len(nodeGraphOutput) > 0:
                                nodeGraphOutputPath = f"{nodeGraphName}/{nodeGraphOutput}"
                                if nodeGraphOutputPath in outputNodes:
                                    outputIndex = outputNodes[nodeGraphOutputPath]
                                else:
                                    self.logger.error(f'> Failed to find output: {nodeGraphOutput} '
                                                      ' in: {outputNodes}')
                                lookup['output'] = outputIndex
                            else:
                                lookup['output'] = 0

                    if 'name' in material:
                        materials.append(material)

        unconnectedGraphs = []
        for ng in mtlxDoc.getNodeGraphs():
            ng_name = ng.getName()
            if ng.getAttribute('nodedef') or ng.hasSourceUri():
                continue
            if ng_name not in exportGraphNames:
                unconnectedGraphs.append(ng_name)

                gltfInfo = self.materialx_graph_to_gltf(ng, json_data, materials)
                procs = gltfInfo[0]
                outputNodes = gltfInfo[1]
                fallbackTextureIndex = gltfInfo[3]

        if len(materials) > 0:
            json_data['materials'] = materials
            if len(unconnectedGraphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnectedGraphs)
        else:
            if len(unconnectedGraphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnectedGraphs)
            else:
                status = 'No appropriate glTF shader graphs found'

        if len(procs) > 0:
            json_data['asset'] = json_asset
            json_data['extensionsUsed'] = extensionsUsed

        jsonString = json.dumps(json_data, indent=2) if json_data else ''
        if jsonString == '{}':
            jsonString = ''

        return jsonString, status

# Utilities

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

def validateDocument(doc):
    '''Validate a MaterialX document.
    @param doc: The document to validate.
    @return: The validation result as a tuple of [valid, errorString].
    '''
    valid, errorString = doc.validate()
    return valid, errorString


