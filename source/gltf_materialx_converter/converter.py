# converter.py

'''
@file converter.py
This module contains the core functionality for MaterialX glTF ProceduralTexture graph conversion.
'''
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

## @var KHR_TEXTURES_BLOCK
## @brief The block for textures.
KHR_TEXTURES_BLOCK = 'textures'

## @var KHR_IMAGES_BLOCK
## @brief The block for images.
KHR_IMAGES_BLOCK = 'images'

## @var KHR_IMAGE_SOURCE
# @brief The block for image sources.
KHR_IMAGE_SOURCE = 'source'

## @var KHR_IMAGE_URI
# @brief The uri attribute for an image block
KHR_IMAGE_URI = 'uri'

## @var KHR_TEXTURE_PROCEDURALS_TYPE
# @brief The attribute for procedural texture type.
KHR_TEXTURE_PROCEDURALS_TYPE = 'type'

## @var KHR_TEXTURE_PROCEDURALS_VALUE
# @brief The attribute for procedural texture uniform values.
KHR_TEXTURE_PROCEDURALS_VALUE = 'value'

## @var KHR_TEXTURE_PROCEDURALS_TEXTURE
# @brief The attribute for procedural texture uniform texture references.
KHR_TEXTURE_PROCEDURALS_TEXTURE = 'texture'

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
## @var MTLX_NODEGRAPH_NAME_ATTRIBUTE
#  @brief Attribute for nodegraph references in MaterialX.
MTLX_NODEGRAPH_NAME_ATTRIBUTE = 'nodegraph'

## @var MTLX_SHADER_PREFIX
#  @brief Prefix for MaterialX shader name generation.
MTLX_SHADER_PREFIX = 'SHD_'

## @var MTLX_INTERFACEINPUT_NAME_ATTRIBUTE
#  @brief Attribute for interface references in MaterialX.
MTLX_INTERFACEINPUT_NAME_ATTRIBUTE = 'interfacename'

## @var MTLX_NODE_NAME_ATTRIBUTE
#  @brief Attribute for node references in MaterialX.
MTLX_NODE_NAME_ATTRIBUTE = 'nodename'

## @var MTLX_NODEDEF_NAME_ATTRIBUTE
#  @brief Attribute for nodegraph references in MaterialX.
MTLX_NODEDEF_NAME_ATTRIBUTE = 'nodedef'

## @var MTLX_OUTPUT_ATTRIBUTE
#  @brief Attribute for outputs in MaterialX.
MTLX_OUTPUT_ATTRIBUTE = 'output'

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
    '''
    @brief Class for converting to convert between glTF Texture Procedurals content and MaterialX
    '''

    def __init__(self):
        '''
        Constructor

        **Attributes**
        - logger : logging.Logger
            - Logger instance for the class, used to log information, warnings, and errors.
        
        - supported_types : list of str
            - List of supported data types. This is fixed to MaterialX 1.39

        - supported_scalar_types : list of str
            - List of supported scalar data types. This is fixed to MaterialX 1.39

        - array_types : list of str
            - List of supported array types. This is fixed to MaterialX 1.39.x

        - metadata : list of str
            - MaterialX and / or 3rd party meta-data to transfer to gltf. Default is MaterialX based metadata for 1.39
        '''
        self.logger = lg.getLogger('glTFMtlx')
        lg.basicConfig(level=lg.INFO)  

        # Options for conversion from Materialx
        self.supported_types = ['boolean', 'string', 'integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_scalar_types = ['integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_array_types = ['matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'color3', 'color4']
        self.supported_metadata = ['colorspace', 'unit', 'unittype', 'uiname', 'uimin', 'uimax', 'uifolder', 'doc', 'xpos', 'ypos']

    def setDebug(self, debug):
        '''
        Set the debug flag for the converter.
        @param debug: The debug flag.
        '''
        if debug:
            self.logger.setLevel(lg.DEBUG)
        else:
            self.logger.setLevel(lg.INFO)

    def setMetaData(self, metadata):
        '''
        Set the supported metadata for the converter.
        @param metadata: The metadata to set.
        '''
        self.supported_metadata = metadata

    def getMetaData(self):
        '''
        Get the supported metadata for the converter.
        @return The metadata.
        '''
        return self.supported_metadata

    def stringToScalar(self, value, type):
        '''
        Convert a supported MaterialX value string to a JSON scalar value.
        @param value: The string value to convert.
        @param type: The type of the value.
        @return The converted scalar value if successful, otherwise the original string value.
        '''
        return_value = value
    
        SCALAR_SEPARATOR = ','
        if type in self.supported_scalar_types:
            split_value = value.split(SCALAR_SEPARATOR)
    
            if len(split_value) > 1:
                return_value = list(map(float, split_value))
            else:
                if type == 'integer':
                    return_value = int(value)
                else:
                    return_value = float(value)
    
        return return_value

    def initializeGLTFTexture(self, texture, name, uri, images):
        '''
        Initialize a new glTF image entry and texture entry which references the image entry.
        
        @param texture: The glTF texture entry to initialize.
        @param name: The name of the texture entry.
        @param uri: The URI of the image entry.
        @param images: The list of images to append the new image entry to.
        '''
        image = {}
        image[KHR_TEXTURE_PROCEDURALS_NAME] = name
    
        # Assuming mx.FilePath and mx.FormatPosix equivalents exist in Python context
        # uri_path = mx.createFilePath(uri)  # Assuming mx.FilePath is a class in the context
        # image[KHR_IMAGE_URI] = uri_path.asString(mx.FormatPosix)  # Assuming asString method and FormatPosix constant exist
        image[KHR_IMAGE_URI] = uri
    
        images.append(image)
    
        texture[KHR_TEXTURE_PROCEDURALS_NAME] = name
        texture[KHR_IMAGE_SOURCE] = len(images) - 1

    def addFallbackTexture(self, json, fallback):
        '''
        Add a fallback texture to the glTF JSON object.
        @param json: The JSON object to add the fallback texture to.
        @param fallback: The fallback texture URI.
        @return The index of the fallback texture if successful, otherwise -1.
        '''
        fallback_texture_index = -1
        fallback_image_index = -1
    
        images_block = json.get(KHR_IMAGES_BLOCK, [])
        if KHR_IMAGES_BLOCK not in json:
            json[KHR_IMAGES_BLOCK] = images_block

        for i, image in enumerate(images_block):
            if image[KHR_IMAGE_URI] == fallback:
                fallback_image_index = i
                break
    
        if fallback_image_index == -1:
            image = {
                KHR_IMAGE_URI: fallback,
                'name': 'KHR_texture_procedural_fallback'
            }
            images_block.append(image)
            fallback_image_index = len(images_block) - 1

        texture_array = json.get(KHR_TEXTURES_BLOCK, [])
        if KHR_TEXTURES_BLOCK not in json:
            json[KHR_TEXTURES_BLOCK] = texture_array

        for i, texture in enumerate(texture_array):
            if texture[KHR_IMAGE_SOURCE] == fallback_image_index:
                fallback_texture_index = i
                break

        if fallback_texture_index == -1:
            texture_array.append({KHR_IMAGE_SOURCE: fallback_image_index})
            fallback_texture_index = len(texture_array) - 1
    
        return fallback_texture_index

    def materialXGraphToGLTF(self, graph, json):
        '''
        Export a MaterialX nodegraph to a glTF procedural graph.
        @param graph: The MaterialX nodegraph to export.
        @param json: The JSON object to export the procedural graph to.
        meaning to export all materials.
        @return The procedural graph JSON object if successful, otherwise None.
        '''
        no_result = [None, None, None]

        graph_outputs = graph.getOutputs()
        if len(graph_outputs) == 0:
            self.logger.info('> No graph outputs found on graph:', graph.getNamePath())
            return no_result

        debug = False
        use_paths = False

        images_block = json.get(KHR_IMAGES_BLOCK, [])
        if KHR_IMAGES_BLOCK not in json:
            json[KHR_IMAGES_BLOCK] = images_block

        texture_array = json.get(KHR_TEXTURES_BLOCK, [])
        if KHR_TEXTURES_BLOCK not in json:
            json[KHR_TEXTURES_BLOCK] = texture_array

        # Dictionaries used to compute index for node, input, and output references.
        # Key is a the path to the items
        nodegraph_nodes = {}
        nodegraph_inputs = {}
        nodegraph_outputs = {}

        # Set up extensions
        extensions = json.get(KHR_EXTENSIONS_BLOCK, {})
        if KHR_EXTENSIONS_BLOCK not in json:
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

        metadata = self.getMetaData()

        # Add nodes to to dictonary. Use path as this is globally unique
        #
        for node in graph.getNodes():
            json_node = {'name': node.getNamePath() if use_paths else node.getName()}
            nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK].append(json_node)
            nodegraph_nodes[node.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK]) - 1

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
                    texture = {}
                    filename = input.getResolvedValueString()
                    # Initialize file texture
                    self.initializeGLTFTexture(texture, input.getNamePath(), filename, images_block)
                    texture_array.append(texture)
                    json_node[KHR_TEXTURE_PROCEDURALS_TEXTURE] = len(texture_array) - 1
                else:
                    value = input.getValueString()
                    value = self.stringToScalar(value, input_type)
                    json_node[KHR_TEXTURE_PROCEDURALS_VALUE] = value
                nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK].append(json_node)

                # Add input to dictionary
                nodegraph_inputs[input.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK]) - 1
            else:
                self.logger.error('> No value or invalid connection specified for input. Input skipped:', input.getNamePath())

        # Add outputs to the graph
        #
        for output in graph_outputs:
            json_node = {KHR_TEXTURE_PROCEDURALS_NAME: output.getNamePath() if use_paths else output.getName()}
            nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK].append(json_node)
            nodegraph_outputs[output.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]) - 1

            json_node[KHR_TEXTURE_PROCEDURALS_NODETYPE] = output.getCategory()
            json_node[KHR_TEXTURE_PROCEDURALS_TYPE] = output.getType()

            # Add additional attributes to the output
            for meta in metadata:
                if output.getAttribute(meta):
                    json_node[meta] = output.getAttribute(meta)

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
                if nodegraph_inputs.get(connection_path) is not None:
                    json_node[KHR_TEXTURE_PROCEDURALS_INPUT] = nodegraph_inputs[connection_path]
                elif nodegraph_nodes.get(connection_path) is not None:
                    json_node[KHR_TEXTURE_PROCEDURALS_NODE] = nodegraph_nodes[connection_path]
                else:
                    self.logger.error(f'> Invalid output connection to: {connection_path}')

                # Add output qualifier if any
                output_string = output.getAttribute(MTLX_OUTPUT_ATTRIBUTE)
                if len(output_string) > 0:
                    json_node[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_string

        # Add nodes to the graph
        for node in graph.getNodes():
            json_node = nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK][nodegraph_nodes[node.getNamePath()]]
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

                        if is_interface and nodegraph_inputs.get(connection_path) is not None:
                            input_item[KHR_TEXTURE_PROCEDURALS_INPUT] = nodegraph_inputs[connection_path]
                        elif nodegraph_nodes.get(connection_path) is not None:
                            input_item[KHR_TEXTURE_PROCEDURALS_NODE] = nodegraph_nodes[connection_path]

                        output_string = input.getAttribute(MTLX_OUTPUT_ATTRIBUTE)
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
                        texture = {}
                        filename = input.getResolvedValueString()
                        self.initializeGLTFTexture(texture, input.getNamePath(), filename, images_block)
                        texture_array.append(texture)
                        input_item[KHR_TEXTURE_PROCEDURALS_TEXTURE] = len(texture_array) - 1
                    else:
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
                    'nodetype': KHR_TEXTURE_PROCEDURALS_OUTPUT,
                    'name': output.getName(),
                    KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                }
                outputs.append(output_item)

            # Add implicit outputs (based on nodedef)
            if nodedef:
                for output in nodedef.getOutputs():
                    if not any(output_item[KHR_TEXTURE_PROCEDURALS_NAME] == output.getName() for output_item in outputs):
                        output_item = {
                            'nodetype': KHR_TEXTURE_PROCEDURALS_OUTPUT,
                            'name': output.getName(),
                            KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                        }
                        outputs.append(output_item)
            else:
                self.logger.warning(f'> Missing nodedef for node: {node.getNamePath()}')

            # Add to node outputs list
            if outputs:
                json_node[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK] = outputs

        return [procs, nodegraph_outputs, nodegraph_nodes]

    def materialXtoGLTF(self, mtlx_doc):
        '''
        @brief Convert a MaterialX document to glTF.
        @param mtlx_doc: The MaterialX document to convert.
        @return glTF JSON string and status message.
        '''

        status = ''
        if not mtlx_doc:
            status = 'Invalid document to convert'
            return None, status

        materials = []
        mx_materials = mtlx_doc.getMaterialNodes()
        if len(mx_materials) == 0:
            self.logger.warning('> No materials found in document')
            #return None, status # No MaterialX materials found in the document

        json_data = {}
        json_asset = {
            "version": "2.0",
            "generator": "MaterialX 1.39 / glTF 2.0 Texture Procedural Converter"
        }

        # Supported input mappings
        input_maps = {}
        input_maps[MTLX_GLTF_PBR_CATEGORY] = [
            # Contains:
            #   <MaterialX input name>, <gltf input name>, [<gltf parent block>]
            ['base_color', 'baseColorTexture', 'pbrMetallicRoughness']
        ]

        pbr_nodes = {}
        fallback_texture_index = -1
        fallback_image_data = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4z/AfAAQAAf/zKSWvAAAAAElFTkSuQmCC'
        procs = []
        export_graph_names = []

        extensions_used = [KHR_TEXTURE_PROCEDURALS, EXT_TEXTURE_PROCEDURALS_MX_1_39]

        # Scan for materials
        for mxMaterial in mx_materials:
            mtlx_shaders = mx.getShaderNodes(mxMaterial)

            # Scan for shaders for the material
            for shader_node in mtlx_shaders:                
                category = shader_node.getCategory()
                path = shader_node.getNamePath()
                is_pbr = (category == MTLX_GLTF_PBR_CATEGORY)

                if (is_pbr) and pbr_nodes.get(path) is None:
                    # Add fallback if not already added
                    if fallback_texture_index == -1:
                        fallback_texture_index = self.addFallbackTexture(json_data, fallback_image_data)

                    self.logger.info(f'> Convert shader to glTF: {shader_node.getNamePath()}. Category: {category}')
                    pbr_nodes[path] = shader_node

                    material = {}

                    material[KHR_TEXTURE_PROCEDURALS_NAME] = path

                    shader_node_input = None
                    shader_node_output = ''
                    input_pairs = input_maps[category]

                    # Scan through support inupt channels
                    for input_pair in input_pairs:
                        shader_node_input = shader_node.getInput(input_pair[0])
                        shader_node_output = input_pair[1]

                        if not shader_node_input:
                            continue

                        # Check for upstream nodegraph connection. Skip if not found
                        nodegraph_name = shader_node_input.getNodeGraphString()
                        if len(nodegraph_name) == 0:
                            continue

                        # Check for upstream nodegraph output connection.
                        nodegraph_output = shader_node_input.getOutputString()

                        # Determine the parent of the input
                        parent = material
                        if len(input_pair[2]) > 0:
                            if input_pair[2] not in material:
                                material[input_pair[2]] = {}
                            parent = material[input_pair[2]]

                        # Check for an existing converted graph and / or output index
                        # in the "procedurals" list
                        graph_index = -1
                        output_index = -1
                        outputs_length = 0
                        if procs:
                            for i, proc in enumerate(procs):
                                if proc[KHR_TEXTURE_PROCEDURALS_NAME] == nodegraph_name:
                                    graph_index = i
                                    outputs_length = len(nodegraph_output) 
                                    if  outputs_length > 0:
                                        for j, output in enumerate(proc[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]):
                                            if output[KHR_TEXTURE_PROCEDURALS_NAME] == nodegraph_output:
                                                output_index = j
                                                break
                                    break

                        # Make the connection to the input on the material if the graph is already converted
                        if graph_index >= 0:
                            shader_input_texture = parent[shader_node_output] = {}
                            shader_input_texture[KHR_TEXTURE_PROCEDURALS_INDEX] = fallback_texture_index
                            ext = shader_input_texture[KHR_EXTENSIONS_BLOCK] = {}

                            # Set up graph index and output index. Only set output index if 
                            # the graph has more than one output
                            lookup = ext[KHR_TEXTURE_PROCEDURALS] = {}                            
                            lookup[KHR_TEXTURE_PROCEDURALS_INDEX] = graph_index
                            if output_index >= 0 and outputs_length > 1:
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_index
                        
                        # Convert the graph
                        else:
                            graph = mtlx_doc.getNodeGraph(nodegraph_name)
                            export_graph_names.append(nodegraph_name)

                            gltf_info = self.materialXGraphToGLTF(graph, json_data)
                            procs = gltf_info[0]
                            output_nodes = gltf_info[1]

                            # Add a fallback texture
                            shader_input_texture = parent[shader_node_output] = {}
                            shader_input_texture[KHR_TEXTURE_PROCEDURALS_INDEX] = fallback_texture_index
                            ext = shader_input_texture[KHR_EXTENSIONS_BLOCK] = {}
                            lookup = ext[KHR_TEXTURE_PROCEDURALS] = {}
                            lookup[KHR_TEXTURE_PROCEDURALS_INDEX] = len(procs) - 1
                            output_index = -1

                            # Assign an output index if the graph has more than one output
                            if len(nodegraph_output) > 0:
                                nodegraph_outputPath = f"{nodegraph_name}/{nodegraph_output}"
                                if nodegraph_outputPath in output_nodes:
                                    output_index = output_nodes[nodegraph_outputPath]
                                else:
                                    self.logger.error(f'> Failed to find output: {nodegraph_output} '
                                                      ' in: {output_nodes}')
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_index
                            else:
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = 0

                    if 'name' in material:
                        materials.append(material)

        # Scan for unconnected graphs
        unconnected_graphs = []
        for ng in mtlx_doc.getNodeGraphs():
            ng_name = ng.getName()
            if ng.getAttribute(MTLX_NODEDEF_NAME_ATTRIBUTE) or ng.hasSourceUri():
                continue
            if ng_name not in export_graph_names:
                unconnected_graphs.append(ng_name)
                gltf_info = self.materialXGraphToGLTF(ng, json_data, materials)
                procs = gltf_info[0]
                output_nodes = gltf_info[1]

        if len(materials) > 0:
            json_data[KHR_MATERIALS_BLOCK] = materials
            if len(unconnected_graphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnected_graphs)
        else:
            if len(unconnected_graphs) > 0:
                status = 'Exported unconnected graphs: ' + ', '.join(unconnected_graphs)
            else:
                status = 'No appropriate glTF shader graphs found'

        # Add asset and extensions use blocks
        if len(procs) > 0:
            json_data[KHR_ASSET_BLOCK] = json_asset
            json_data[KHR_EXTENTIONSUSED_BLOCK] = extensions_used

        # Get the JSON string back
        json_string = json.dumps(json_data, indent=2) if json_data else ''
        if json_string == '{}':
            json_string = ''

        return json_string, status


