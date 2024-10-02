# converter.py

'''
@file converter.py
This module contains the core functionality for MaterialX glTF ProceduralTexture graph conversion.
'''
import os, argparse
import json
import MaterialX as mx
import logging as lg 

'''
Package globals
'''
## @var KHR_TEXTURE_PROCEDURALS
#  @brief Extension name for KHR_texture_procedurals.
KHR_TEXTURE_PROCEDURALS = 'KHR_texture_procedurals'


## @var EXT_TEXTURE_PROCEDURALS_MX_1_39
#  @brief Extension name for EXT_texture_procedurals_mx_1_39.
EXT_TEXTURE_PROCEDURALS_MX_1_39 = 'EXT_texture_procedurals_mx_1_39'

## @var KHR_MATERIALX_UNLIT
#  @brief Extension name for KHR_materials_unlit.
KHR_MATERIALX_UNLIT = 'KHR_materials_unlit'

## @var KHR_EXTENSIONS_BLOCK
# @brief The block for extensions.
KHR_EXTENSIONS_BLOCK = 'extensions'

## @var KHR_EXTENTIONSUSED_BLOCK
# @brief The block for used extensions.
KHR_EXTENTIONSUSED_BLOCK = 'extensionsUsed'

## @var KHR_ASSET_BLOCK
# @brief The block for asset information.
KHR_ASSET_BLOCK = 'asset'

## @var KHR_MATERIALS_BLOCK
# @brief The block for materials.
KHR_MATERIALS_BLOCK = 'materials'

## @var KHR_IMAGE_SOURCE
# @brief The block for image sources.
KHR_IMAGE_SOURCE = 'source'

## @var KHR_TEXTURE_PROCEDURALS_TYPE
# @brief The attribute for procedural texture type.
KHR_TEXTURE_PROCEDURALS_TYPE = 'type'

## @var KHR_TEXTURE_PROCEDURALS_VALUE
# @brief The attribute for procedural texture value.
KHR_TEXTURE_PROCEDURALS_VALUE = 'value'

## @var KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK
# @brief The block for procedural texture inputs.
KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK = 'inputs'

## @var KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK
# @brief The block for procedural texture outputs.
KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK = 'outputs'

## @var KHR_TEXTURE_PROCEDURALS_NODES_BLOCK
# @brief The block for procedural texture nodes.
KHR_TEXTURE_PROCEDURALS_NODES_BLOCK = 'nodes'

## @var KHR_TEXTURE_PROCEDURALS_NODETYPE
# @brief The attribute for procedural texture node type.
KHR_TEXTURE_PROCEDURALS_NODETYPE = 'nodetype'

## @var KHR_TEXTURE_PROCEDURALS_NAME
# @brief The attribute for procedural texture name.
KHR_TEXTURE_PROCEDURALS_NAME = 'name'

## @var KHR_TEXTURE_PROCEDURALS_INPUT
# @brief The attribute for procedural texture input.
KHR_TEXTURE_PROCEDURALS_INPUT = 'input'

## @var KHR_TEXTURE_PROCEDURALS_OUTPUT
# @brief The attribute for procedural texture output.
KHR_TEXTURE_PROCEDURALS_OUTPUT = 'output'

## @var KHR_TEXTURE_PROCEDURALS_NODE
# @brief The attribute for procedural texture node.
KHR_TEXTURE_PROCEDURALS_NODE = 'node'

## @var KHR_TEXTURE_PROCEDURALS_INDEX
# @brief The attribute for procedural texture index.
KHR_TEXTURE_PROCEDURALS_INDEX = 'index'

## @var KHR_TEXTURE_PROCEDURALS_NODEGROUP
# @brief The attribute for procedural texture node group.
KHR_TEXTURE_PROCEDURALS_NODEGROUP = 'nodegroup'

## @var KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK
# @brief The block for procedural textures.
KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK = 'procedurals'

## @var MTLX_DEFAULT_MATERIAL_NAME
#  @brief Default name for a MaterialX material generation.
MTLX_DEFAULT_MATERIAL_NAME = 'MAT_0'

## @var MTLX_MATERIAL_PREFIX
#  @brief Prefix for MaterialX material name generation.
MTLX_MATERIAL_PREFIX = 'MAT_'

## @var MTLX_DEFAULT_SHADER_NAME
#  @brief Default name for a MaterialX shader generation.
MTLX_DEFAULT_SHADER_NAME = 'SHD_0'

## @var MTLX_SHADER_PREFIX
#  @brief Prefix for MaterialX shader name generation.
MTLX_SHADER_PREFIX = 'SHD_'

## @var MTLX_INTERFACEINPUT_NAME_ATTRIBUTE
#  @brief Attribute for interface references in MaterialX.
MTLX_INTERFACEINPUT_NAME_ATTRIBUTE = 'interfacename'

## @var MTLX_NODE_NAME_ATTRIBUTE
#  @brief Attribute for node references in MaterialX.
MTLX_NODE_NAME_ATTRIBUTE = 'nodename'

## @var MTLX_NODEGRAPH_NAME_ATTRIBUTE
#  @brief Attribute for nodegraph references in MaterialX.
MTLX_NODEGRAPH_NAME_ATTRIBUTE = 'nodegraph'

## @var MTLX_GLTF_PBR_CATEGORY
#  @brief Category string for glTF PBR shading model in MaterialX.
MTLX_GLTF_PBR_CATEGORY = 'gltf_pbr'

## @var MTLX_UNLIT_CATEGORY_STRING
#  @brief Category string for unlit surface shading model in MaterialX.
MTLX_UNLIT_CATEGORY_STRING = 'surface_unlit'

## @var MULTI_OUTPUT_TYPE_STRING
#  @brief String identifier for multi-output types in MaterialX.
MULTI_OUTPUT_TYPE_STRING = 'multioutput'

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
    
    def stringToScalar(self, value, type):
        """
        Convert a supported MaterialX value string to a JSON scalar value.
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

    def materialXGraphToGLTF(self, graph, json, materials):
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

        # Create fallback texture. Separate out
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
            if texture[KHR_IMAGE_SOURCE] == fallback_index:
                fallback_texture_index = i
                break

        if fallback_texture_index == -1:
            texture_array.append({KHR_IMAGE_SOURCE: fallback_index})
            fallback_texture_index = len(texture_array) - 1

        proc_dict_nodes = {}
        proc_dict_inputs = {}
        proc_dict_outputs = {}

        # Set up extensions
        extensions = json.get('extensions', {})
        if 'extensions' not in json:
            json[KHR_EXTENSIONS_BLOCK] = extensions

        KHR_texture_procedurals = extensions.get(KHR_TEXTURE_PROCEDURALS, {})
        if KHR_TEXTURE_PROCEDURALS not in extensions:
            extensions[KHR_TEXTURE_PROCEDURALS] = KHR_texture_procedurals

        if KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK not in KHR_texture_procedurals:
            KHR_texture_procedurals[KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK] = []

        procs = KHR_texture_procedurals[KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK]
        nodegraph = {
            'name': graph.getNamePath() if use_paths else graph.getName(),
            'nodetype': graph.getCategory()
        }

        nodegraph[KHR_TEXTURE_PROCEDURALS_TYPE] = MULTI_OUTPUT_TYPE_STRING if len(graph_outputs) > 1 else graph_outputs[0].getType()
        nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK] = []
        nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK] = []
        nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK] = []
        procs.append(nodegraph)

        # Setup supported metadata
        metadata = ['colorspace', 'unit', 'unittype', 'uiname', 'uimin', 'uimax', 'uifolder', 'doc']

        # Add nodes to to dictonary. Use path as this is globally unique
        #
        for node in graph.getNodes():
            json_node = {'name': node.getNamePath() if use_paths else node.getName()}
            nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK].append(json_node)
            proc_dict_nodes[node.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK]) - 1

        # Add inputs to the graph
        #
        for input in graph.getInputs():
            json_node = {
                'name': input.getNamePath() if use_paths else input.getName(),
                'nodetype': input.getCategory()
            }

            for meta in metadata:
                if input.getAttribute(meta):
                    json_node[meta] = input.getAttribute(meta)

            # Only values are allowed for graph inputs
            if input.getValue() is not None:
                input_type = input.getAttribute(mx.TypedElement.TYPE_ATTRIBUTE)
                json_node[KHR_TEXTURE_PROCEDURALS_TYPE] = input_type
                if input_type == mx.FILENAME_TYPE_STRING:
                    self.logger.warning('> File texture inputs not supported:', input.getNamePath())

                value = input.getValueString()
                value = self.stringToScalar(value, input_type)
                json_node['value'] = value
                nodegraph['inputs'].append(json_node)

                # Add input to dictionary
                proc_dict_inputs[input.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK]) - 1
            else:
                self.logger.error('> No value or invalid connection specified for input. Input skipped:', input.getNamePath())

        # Add outputs to the graph
        #
        for output in graph_outputs:
            json_node = {KHR_TEXTURE_PROCEDURALS_NAME: output.getNamePath() if use_paths else output.getName()}
            nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK].append(json_node)
            proc_dict_outputs[output.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]) - 1

            json_node[KHR_TEXTURE_PROCEDURALS_NODETYPE] = output.getCategory()
            json_node[KHR_TEXTURE_PROCEDURALS_TYPE] = output.getType()

            # Add connection if any. Only interfacename and nodename
            # are supported.
            connection = output.getAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE)
            if len(connection) == 0:
                connection = output.getAttribute(MTLX_NODE_NAME_ATTRIBUTE)

            connection_node = graph.getChild(connection)
            if connection_node:
                connection_path = connection_node.getNamePath()
                if debug:
                    json_node['debug_connection_path'] = connection_path

                # Add an input or node connection
                if proc_dict_inputs.get(connection_path) is not None:
                    json_node[KHR_TEXTURE_PROCEDURALS_INPUT] = proc_dict_inputs[connection_path]
                elif proc_dict_nodes.get(connection_path) is not None:
                    json_node[KHR_TEXTURE_PROCEDURALS_NODE] = proc_dict_nodes[connection_path]
                else:
                    self.logger.error(f'> Invalid output connection to: {connection_path}')

                # Add output qualifier if any
                output_string = output.getAttribute('output')
                if len(output_string) > 0:
                    json_node[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_string

        # Add nodes to the graph
        for node in graph.getNodes():
            json_node = nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK][proc_dict_nodes[node.getNamePath()]]
            json_node[KHR_TEXTURE_PROCEDURALS_NODETYPE] = node.getCategory()
            nodedef = node.getNodeDef()

            # Skip unsupported nodes
            if not nodedef:
                self.logger.error(f'> Missing nodedef for node: {node.getNamePath()}')
                continue

            if debug and nodedef and nodedef.getNodeGroup():
                json_node[KHR_TEXTURE_PROCEDURALS_NODEGROUP] = nodedef.getNodeGroup()

            for attr_name in node.getAttributeNames():
                json_node[attr_name] = node.getAttribute(attr_name)

            # Add node inputs
            #
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
                input_item[KHR_TEXTURE_PROCEDURALS_TYPE] = input_type

                # Add connection. Connections superscede values.
                # Only interfacename and nodename are supported.                
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
                            input_item[KHR_TEXTURE_PROCEDURALS_INPUT] = proc_dict_inputs[connection_path]
                        elif proc_dict_nodes.get(connection_path) is not None:
                            input_item[KHR_TEXTURE_PROCEDURALS_NODE] = proc_dict_nodes[connection_path]

                        output_string = input.getAttribute('output')
                        if output_string:
                            connected_node_outputs = connection_node.getOutputs()
                            for i, connected_output in enumerate(connected_node_outputs):
                                if connected_output.getName() == output_string:
                                    input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT] = i
                                    break
                    else:
                        self.logger.error(f'> Invalid input connection to: '
                                            '{connection} from input: {input.getNamePath()} '
                                            'node: {node.getNamePath()}')

                # Node input value if any
                elif input.getValue() is not None:
                    if input_type == mx.FILENAME_TYPE_STRING:
                        self.logger.warning('> File texture inputs not supported:', input.getNamePath())

                    value = input.getValueString()
                    value = self.stringToScalar(value, input_type)
                    input_item[KHR_TEXTURE_PROCEDURALS_VALUE] = value

                inputs.append(input_item)

            # Add node inputs list
            if inputs:
                json_node[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK] = inputs

            # Find explicit node outputs
            outputs = []
            for output in node.getOutputs():
                output_item = {
                    'nodetype': 'output',
                    'name': output.getName(),
                    KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                }
                outputs.append(output_item)

            # Add implicit outputs (based on nodedef)
            if nodedef:
                for output in nodedef.getOutputs():
                    if not any(output_item[KHR_TEXTURE_PROCEDURALS_NAME] == output.getName() for output_item in outputs):
                        output_item = {
                            'nodetype': 'output',
                            'name': output.getName(),
                            KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                        }
                        outputs.append(output_item)
            else:
                self.logger.warning(f'> Missing nodedef for node: {node.getNamePath()}')

            # Add to node outputs list
            if outputs:
                json_node[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK] = outputs

        return [procs, proc_dict_outputs, proc_dict_nodes, fallback_texture_index]

    def materialXtoGLTF(self, mtlxDoc):
        """
        @brief Convert a MaterialX document to glTF.
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
            "generator": "MaterialX 1.39 / glTF 2.0 Texture Procedural Converter"
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

        extensionsUsed = [KHR_TEXTURE_PROCEDURALS, EXT_TEXTURE_PROCEDURALS_MX_1_39]

        # Scan for materials
        for mxMaterial in mxMaterials:
            mxshaders = mx.getShaderNodes(mxMaterial)

            # Scan for shaders for the material
            for shaderNode in mxshaders:
                category = shaderNode.getCategory()
                path = shaderNode.getNamePath()
                isPBR = (category == MTLX_GLTF_PBR_CATEGORY)
                if (isPBR) and pbrNodes.get(path) is None:
                    self.logger.info(f'> Convert shader to glTF: {shaderNode.getNamePath()}. Category: {category}')
                    pbrNodes[path] = shaderNode

                    material = {}

                    material[KHR_TEXTURE_PROCEDURALS_NAME] = path

                    base_color_input = None
                    base_color_output = ''
                    inputPairs = inputMaps[category]

                    # Scan through support inupt channels
                    for inputPair in inputPairs:
                        base_color_input = shaderNode.getInput(inputPair[0])
                        base_color_output = inputPair[1]

                        if not base_color_input:
                            continue

                        # Check for upstream nodegraph connection. Skip if not found
                        nodeGraphName = base_color_input.getNodeGraphString()
                        if len(nodeGraphName) == 0:
                            continue

                        # Check for upstream nodegraph output connection.
                        nodeGraphOutput = base_color_input.getOutputString()

                        # Determine the parent of the input
                        parent = material
                        if len(inputPair[2]) > 0:
                            if inputPair[2] not in material:
                                material[inputPair[2]] = {}
                            parent = material[inputPair[2]]

                        # Check for an existing converted graph and / or output index
                        # in the "procedurals" list
                        graphIndex = -1
                        outputIndex = -1
                        if procs:
                            for i, proc in enumerate(procs):
                                if proc[KHR_TEXTURE_PROCEDURALS_NAME] == nodeGraphName:
                                    graphIndex = i
                                    if len(nodeGraphOutput) > 0:
                                        for j, output in enumerate(proc[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]):
                                            if output[KHR_TEXTURE_PROCEDURALS_NAME] == nodeGraphOutput:
                                                outputIndex = j
                                                break
                                    break

                        # Make the connection to the input on the material if the graph is already converted
                        if graphIndex >= 0:
                            baseColorTexture = parent[base_color_output] = {}
                            baseColorTexture[KHR_TEXTURE_PROCEDURALS_INDEX] = fallbackTextureIndex
                            ext = baseColorTexture[KHR_EXTENSIONS_BLOCK] = {}

                            # Set up graph index and output index. Only set output index if 
                            # the graph has more than one output
                            lookup = ext[KHR_TEXTURE_PROCEDURALS] = {}                            
                            lookup[KHR_TEXTURE_PROCEDURALS_INDEX] = graphIndex
                            if outputIndex >= 0 and outputsLength > 1:
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = outputIndex
                        
                        # Convert the graph
                        else:
                            graph = mtlxDoc.getNodeGraph(nodeGraphName)
                            exportGraphNames.append(nodeGraphName)

                            gltfInfo = self.materialXGraphToGLTF(graph, json_data, materials)
                            procs = gltfInfo[0]
                            outputNodes = gltfInfo[1]
                            fallbackTextureIndex = gltfInfo[3]

                            # Add a fallback texture
                            baseColorTexture = parent[base_color_output] = {}
                            baseColorTexture[KHR_TEXTURE_PROCEDURALS_INDEX] = fallbackTextureIndex
                            ext = baseColorTexture[KHR_EXTENSIONS_BLOCK] = {}
                            lookup = ext[KHR_TEXTURE_PROCEDURALS] = {}
                            lookup[KHR_TEXTURE_PROCEDURALS_INDEX] = len(procs) - 1
                            outputIndex = -1

                            # Assign an output index if the graph has more than one output
                            if len(nodeGraphOutput) > 0:
                                nodeGraphOutputPath = f"{nodeGraphName}/{nodeGraphOutput}"
                                if nodeGraphOutputPath in outputNodes:
                                    outputIndex = outputNodes[nodeGraphOutputPath]
                                else:
                                    self.logger.error(f'> Failed to find output: {nodeGraphOutput} '
                                                      ' in: {outputNodes}')
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = outputIndex
                            else:
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = 0

                    if 'name' in material:
                        materials.append(material)

        # Scan for unconnected graphs
        unconnectedGraphs = []
        for ng in mtlxDoc.getNodeGraphs():
            ng_name = ng.getName()
            if ng.getAttribute('nodedef') or ng.hasSourceUri():
                continue
            if ng_name not in exportGraphNames:
                unconnectedGraphs.append(ng_name)
                gltfInfo = self.materialXGraphToGLTF(ng, json_data, materials)
                procs = gltfInfo[0]
                outputNodes = gltfInfo[1]
                fallbackTextureIndex = gltfInfo[3]

        if len(materials) > 0:
            json_data[KHR_MATERIALS_BLOCK] = materials
            if len(unconnectedGraphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnectedGraphs)
        else:
            if len(unconnectedGraphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnectedGraphs)
            else:
                status = 'No appropriate glTF shader graphs found'

        # Add asset and extensions use blocks
        if len(procs) > 0:
            json_data[KHR_ASSET_BLOCK] = json_asset
            json_data[KHR_EXTENTIONSUSED_BLOCK] = extensionsUsed

        # Get the JSON string back
        jsonString = json.dumps(json_data, indent=2) if json_data else ''
        if jsonString == '{}':
            jsonString = ''

        return jsonString, status


