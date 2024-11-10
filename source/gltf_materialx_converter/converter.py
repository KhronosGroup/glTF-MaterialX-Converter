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
        
        - add_comments : bool
            - Option to add comments during the conversion to MaterialX.
        
        - add_nodedef_strings : bool
            - Option to add node definition strings during the conversion to MaterialX.
        
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

        # Options for conversion to MaterialX
        self.add_comments = False
        self.add_nodedef_strings = False

        # Options for conversion from Materialx
        self.supported_types = ['boolean', 'string', 'integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_scalar_types = ['integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_array_types = ['matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'color3', 'color4']
        self.supported_metadata = ['colorspace', 'unit', 'unittype', 'uiname', 'uimin', 'uimax', 'uifolder', 'doc', 'xpos', 'ypos']

    def set_debug(self, debug):
        '''
        Set the debug flag for the converter.
        @param debug: The debug flag.
        '''
        if debug:
            self.logger.setLevel(lg.DEBUG)
        else:
            self.logger.setLevel(lg.INFO)

    def set_metadata(self, metadata):
        '''
        Set the supported metadata for the converter.
        @param metadata: The metadata to set.
        '''
        self.supported_metadata = metadata

    def get_metadata(self):
        '''
        Get the supported metadata for the converter.
        @return The metadata.
        '''
        return self.supported_metadata

    def get_supported_target_type(self):
        '''
        Get the target type that MaterialX can be converted to.
        @return The target type supported by the converter.
        '''
        return 'gltf'

    def get_supported_source_type(self):
        '''
        Get the source type thay can be converted to MaterialX.
        @return The source type supported by the converter.
        '''
        return 'gltf'

    def string_to_scalar(self, value, type):
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

    def initialize_glTF_texture(self, texture, name, uri, images):
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

    def add_fallback_texture(self, json, fallback):
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
                KHR_TEXTURE_PROCEDURALS_NAME: 'KHR_texture_procedural_fallback'
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

    def materialX_graph_to_glTF(self, graph, json):
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
            self.logger.info(f'> No graph outputs found on graph: {graph.getNamePath()}')
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

        metadata = self.get_metadata()

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
                    self.initialize_glTF_texture(texture, input.getNamePath(), filename, images_block)
                    texture_array.append(texture)
                    json_node[KHR_TEXTURE_PROCEDURALS_TEXTURE] = len(texture_array) - 1
                else:
                    value = input.getValueString()
                    value = self.string_to_scalar(value, input_type)
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
                        self.initialize_glTF_texture(texture, input.getNamePath(), filename, images_block)
                        texture_array.append(texture)
                        input_item[KHR_TEXTURE_PROCEDURALS_TEXTURE] = len(texture_array) - 1
                    else:
                        value = input.getValueString()
                        value = self.string_to_scalar(value, input_type)
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

    def materialX_to_glTF(self, mtlx_doc):
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
                        fallback_texture_index = self.add_fallback_texture(json_data, fallback_image_data)

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

                            gltf_info = self.materialX_graph_to_glTF(graph, json_data)
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

                    if KHR_TEXTURE_PROCEDURALS_NAME in material:
                        materials.append(material)

        # Scan for unconnected graphs
        unconnected_graphs = []
        for ng in mtlx_doc.getNodeGraphs():
            ng_name = ng.getName()
            if ng.getAttribute(MTLX_NODEDEF_NAME_ATTRIBUTE) or ng.hasSourceUri():
                continue
            if ng_name not in export_graph_names:
                unconnected_graphs.append(ng_name)
                gltf_info = self.materialX_graph_to_glTF(ng, json_data)
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

        # if images is empty remove it
        images_block = json_data.get(KHR_IMAGES_BLOCK, [])
        if len(images_block) == 0:
            json_data.pop(KHR_IMAGES_BLOCK, None)
        # if textures is empty remove it
        textures_block = json_data.get(KHR_TEXTURES_BLOCK, [])
        if len(textures_block) == 0:
            json_data.pop(KHR_TEXTURES_BLOCK, None)

        # Add asset and extensions use blocks
        if procs and len(procs) > 0:
            json_data[KHR_ASSET_BLOCK] = json_asset
            json_data[KHR_EXTENTIONSUSED_BLOCK] = extensions_used

            # Get the JSON string back
            json_string = json.dumps(json_data, indent=2) if json_data else ''
            if json_string == '{}':
                json_string = ''
        else:
            json_string = ''
            status = 'No procedural graphs converted'

        return json_string, status

    ############################
    # glTF to MaterialX methods
    ############################

    def set_add_xml_comments(self, add_comments):
        '''
        Set the flag to add comments to the generated MaterialX files.
        @param add_comments: The flag to add comments.
        '''
        self.add_comments = add_comments

    def set_add_nodedef_strings(self, add_nodedef_strings):
        '''
        Set the flag to add nodedef strings to the generated MaterialX files.
        @param add_nodedef_strings: The flag to add nodedef strings.
        '''
        self.add_nodedef_strings = add_nodedef_strings      
        
    def scalar_to_string(self, value, type):
        '''
        Convert a scalar value to a string value that is supported by MaterialX.
        @param value: The scalar value to convert.
        @param type: The type of the value.
        @return The converted string value, or None if the type is unsupported.
        '''
        return_value = None
        if type in self.supported_types:
            if type in self.supported_array_types:
                return_value = ', '.join(map(lambda x: ('{0:g}'.format(x) if isinstance(x, float) else str(x)), value))
            else:
                return_value = '{0:g}'.format(value) if isinstance(value, float) else str(value)            
        else:
            self.logger.warning(f'> Unsupported type:"{type}" not found in supported list: {self.supported_types}')

        return return_value

    def get_glTF_texture_uri(self, texture, images):
        '''
        Get the URI of a glTF texture.
        
        @param texture: The glTF texture.
        @param images: The set of glTF images.
        @return The URI of the texture.
        '''
        uri = ''
        if texture and KHR_IMAGE_SOURCE in texture:
            source = texture[KHR_IMAGE_SOURCE]
            if source < len(images):
                image = images[source]
                if 'uri' in image:
                    uri = image['uri']
        return uri

    def add_inputs_from_nodedef(self, node, node_def):
        '''
        Add inputs to a node from a given MaterialX node definition.
        
        @param node: The MaterialX node to add inputs to.
        @param node_def: The MaterialX node definition to add inputs from.
        @return The updated MaterialX node.
        '''
        if node_def:
            for node_def_input in node_def.getActiveInputs():
                input_name = node_def_input.getName()
                node_input = node.getInput(input_name)
                if not node_input:
                    node_input = node.addInput(input_name, node_def_input.getType())
                    if node_def_input.hasValueString():
                        node_input.setValueString(node_def_input.getValueString())
                        node_input.setType(node_def_input.getType())
        return node

    def have_procedural_tex_extensions(self, glTFDoc):
        '''
        Does the glTF document have the required procedural texture extensions.
        
        @param glTFDoc: The glTF document to check.
        @return The result of the check in the form [boolean, string], where "boolean" is true if the extensions are present,
                 and "string" is an error message if the extensions are not present.
        '''
        # Check extensionsUsed for KHR_texture_procedurals
        extensions_used = glTFDoc.get('extensionsUsed', None)
        if extensions_used is None:
            return [None, 'No extension used']
        
        found = [False, False]
        for ext in extensions_used:
            if ext == KHR_TEXTURE_PROCEDURALS:
                found[0] = True
            if ext == EXT_TEXTURE_PROCEDURALS_MX_1_39:
                found[1] = True
        
        if not found[0]:
            return [None, f'Missing {KHR_TEXTURE_PROCEDURALS} extension']
        if not found[1]:
            return [None, f'Missing{EXT_TEXTURE_PROCEDURALS_MX_1_39} extension']
        
        return [True, '']

    def glTF_to_materialX(self, glTFDoc, stdlib):
        '''
        Convert a glTF document to a MaterialX document.
        @param gltFDoc: The glTF document to import.
        @param stdlib: The MateriaLX standard library to use for the conversion.
        @return The MaterialX document if successful, otherwise None.
        '''
        if not glTFDoc:
            self.logger.error('> No glTF document specified')
            return None

        extension_check = self.have_procedural_tex_extensions(glTFDoc)
        if extension_check[0] is None:
            return None

        doc = mx.createDocument()
        doc.setAttribute('colorspace', 'lin_rec709')

        # Import the graph
        self.glTF_graph_to_materialX(doc, glTFDoc)

        global_extensions = glTFDoc.get('extensions', None)
        procedurals = None
        if global_extensions and KHR_TEXTURE_PROCEDURALS in global_extensions:
            procedurals = global_extensions[KHR_TEXTURE_PROCEDURALS].get(KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK, None)
            #self.logger.debug(f'Imported all procedurals: {procedurals}')

        # Import materials and connect to graphs as needed
        shaderName = MTLX_DEFAULT_SHADER_NAME
        materialName = MTLX_DEFAULT_MATERIAL_NAME
        materialIndex = 1
        glTFmaterials = glTFDoc.get(KHR_MATERIALS_BLOCK, None)
        if glTFmaterials:

            input_maps = {}
            input_maps[MTLX_GLTF_PBR_CATEGORY] = [
                ['base_color', 'baseColorTexture', 'pbrMetallicRoughness']
            ]

            for glTFmaterial in glTFmaterials:

                mtlxShaderName = glTFmaterial.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                mtlxMaterialName = ''
                if len(mtlxShaderName) == 0:
                    mtlxShaderName = shaderName + str(materialIndex)
                    mtlxMaterialName = materialName + str(materialIndex)
                    materialIndex += 1
                else:
                    mtlxMaterialName = 'MAT_' + mtlxShaderName
                
                mtlxShaderName = doc.createValidChildName(mtlxShaderName)
                mtlxMaterialName = doc.createValidChildName(mtlxMaterialName)

                extensions = glTFmaterial.get('extensions', None)

                shaderCategory = MTLX_GLTF_PBR_CATEGORY
                nodedefString = 'ND_gltf_pbr_surfaceshader'
                
                if self.add_comments:
                    comment = doc.addChildOfCategory('comment')
                    comment.setDocString('Generated shader: ' + mtlxShaderName)
                shaderNode = doc.addNode(shaderCategory, mtlxShaderName, mx.SURFACE_SHADER_TYPE_STRING)

                if self.add_nodedef_strings:
                    shaderNode.setAttribute(mx.InterfaceElement.NODE_DEF_ATTRIBUTE, nodedefString)
                else:
                    shaderNode.removeAttribute(mx.InterfaceElement.NODE_DEF_ATTRIBUTE)
                
                # No need to add all inputs from nodedef.
                # In fact if there is a defaultgeomprop then it will be added automatically
                # without any value or connection which causes a validation error.
                #if stdlib:
                    #odedef = stdlib.getNodeDef(nodedefString)
                    #if nodedef:
                    #    self.add_inputs_from_nodedef(shaderNode, nodedef)

                if procedurals:
                    currentMap = input_maps[shaderCategory]
                    for map_item in currentMap:
                        destInput = map_item[0]
                        sourceTexture = map_item[1]
                        sourceParent = map_item[2]
        
                        if sourceParent:
                            if sourceParent == 'pbrMetallicRoughness':
                                if 'pbrMetallicRoughness' in glTFmaterial:
                                    sourceTexture = glTFmaterial['pbrMetallicRoughness'].get(sourceTexture, None)
                                else:
                                    sourceTexture = None
                        else:
                            sourceTexture = glTFmaterial.get(sourceTexture, None)

                        baseColorTexture = sourceTexture

                        if baseColorTexture:
                            extensions = baseColorTexture.get('extensions', None)
                            if extensions and KHR_TEXTURE_PROCEDURALS in extensions:
                                KHR_texture_procedurals = extensions[KHR_TEXTURE_PROCEDURALS]
                                pindex = KHR_texture_procedurals.get('index', None)
                                output = KHR_texture_procedurals.get('output', None)
                                
                                if pindex is not None and pindex < len(procedurals):
                                    proc = procedurals[pindex]
                                    if proc:
                                        nodegraphName = proc.get('name', 'nodegraph')
                                        graphOutputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, None)
                                        outputCount = len(graphOutputs)
                                        if graphOutputs:
                                            proc_output = graphOutputs[0]
                                            if output is not None:
                                                proc_output = graphOutputs[output]
                                            
                                            if proc_output:
                                                input_node = shaderNode.getInput(destInput)
                                                if not input_node:
                                                    input_node = shaderNode.addInput(destInput, proc_output[KHR_TEXTURE_PROCEDURALS_TYPE])
                                                
                                                if input_node:
                                                    input_node.removeAttribute('value')
                                                    input_node.setNodeGraphString(nodegraphName)
                                                    if outputCount > 1:
                                                        input_node.setAttribute('output', proc_output[KHR_TEXTURE_PROCEDURALS_NAME])

                if self.add_comments:
                    comment = doc.addChildOfCategory('comment')
                    comment.setDocString('Generated material: ' + mtlxMaterialName)
                materialNode = doc.addNode(mx.SURFACE_MATERIAL_NODE_STRING, mtlxMaterialName, mx.MATERIAL_TYPE_STRING)
                shaderInput = materialNode.addInput(mx.SURFACE_SHADER_TYPE_STRING, mx.SURFACE_SHADER_TYPE_STRING)
                shaderInput.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, mtlxShaderName)

                self.logger.info(f'> Import material: {materialNode.getName()}. Shader: {shaderNode.getName()}')

        # Import asset information
        if self.add_comments:
            asset = glTFDoc.get('asset', None)
            docDoc = ''
            if asset:
                version = asset.get('version', None)
                if version:
                    comment = doc.addChildOfCategory('comment')
                    docDoc += f'glTF version: {version}. '
                    comment.setDocString(f'glTF version: {version}')

                generator = asset.get('generator', None)
                if generator:
                    comment = doc.addChildOfCategory('comment')
                    docDoc += f'glTF generator: {generator}. '
                    comment.setDocString(f'glTF generator: {generator}')

                copyRight = asset.get('copyright', None)
                if copyRight:
                    comment = doc.addChildOfCategory('comment')
                    docDoc += f'Copyright: {copyRight}. '
                    comment.setDocString(f'Copyright: {copyRight}')

                if docDoc:
                    doc.setAttribute('doc', docDoc)

        return doc      
    
    def glTF_graph_to_materialX(self, doc, gltf_doc):
        '''
        Import the procedural graphs from a glTF document into a MaterialX document.
        @param doc: The MaterialX document to import the graphs into.
        @param gltf_doc: The glTF document to import the graphs from.
        @return The root MaterialX nodegraph if successful, otherwise None.
        '''
        root_mtlx = None

        # Look for the extension
        extensions = gltf_doc.get('extensions', None)
        procedurals = None
        if extensions:
            procedurals = extensions.get(KHR_TEXTURE_PROCEDURALS, {}).get(KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK, None)

        if procedurals is None:
            self.logger.error('> No procedurals array found')
            return None

        metadata = self.get_metadata()

        # Pre and postfix for automatic graph name generation
        GRAPH_PREFIX = 'nodegraph_'
        graph_index = 0

        self.logger.info(f'> Importing {len(procedurals)} procedural graphs')
        for proc in procedurals:
            self.logger.debug(f'> Scan procedural {graph_index} of {len(procedurals)} :')
            if not proc.get('nodetype'):
                self.logger.warning('>  No nodetype found in procedural. Skipping node')
                continue

            if proc[KHR_TEXTURE_PROCEDURALS_NODETYPE] != 'nodegraph':
                self.logger.warning(f'> Unsupported procedural nodetype found: {proc["nodetype"]}')
                continue

            graph_name = proc.get('name', 'graph_' + str(graph_index))
            if 'name' not in proc:
                proc['name'] = graph_name
                graph_index += 1
            
            # Create new nodegraph
            self.logger.info(f'> Create new nodegraph: {graph_name}')
            mtlx_graph = doc.addNodeGraph(graph_name)
            root_mtlx = mtlx_graph

            # Counters for automatic input, output and node name generation
            INPUT_PREFIX = 'input_'
            input_index = 0
            output_index = 0
            node_index = 0

            inputs = proc.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, [])
            outputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, [])
            nodes = proc.get(KHR_TEXTURE_PROCEDURALS_NODES_BLOCK, [])

            # Scan for input interfaces in the node graph
            # Prelable inputs
            for input_item in inputs:
                inputname = input_item.get('name', 'input_' + str(input_index))
                if 'name' not in input_item:
                    input_item['name'] = inputname
                    input_index += 1

            self.logger.debug(f'> Scan {len(inputs)} inputs')
            for input_item in inputs:
                inputname = input_item.get('name', 'input_' + str(input_index))

                # A type is required
                input_type = input_item.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                if not input_type:
                    self.logger.error(f'> Input type not found for graph input: {inputname}')
                    continue

                # Add new interface input
                mtlx_input = mtlx_graph.addInput(inputname, input_type)
                # Set metadata. TODO: Add more than colorspace
                if 'colorspace' in input_item:
                    mtlx_input.setAttribute('colorspace', input_item['colorspace'])

                # If input is a file reference, examines textures and images to retrieve the URI
                if input_type == 'filename':
                    texture_index = input_item.get('texture', None)
                    if texture_index is not None:
                        gltf_textures = gltf_doc.get('textures', None)
                        gltf_images = gltf_doc.get('images', None)
                        if gltf_textures and gltf_images:
                            gltf_texture = gltf_textures[texture_index] if texture_index < len(gltf_textures) else None
                            if gltf_texture:
                                uri = self.get_glTF_texture_uri(gltf_texture, gltf_images)
                                mtlx_input.setValueString(uri, input_type)

                # If input has a value, set the value
                input_value = input_item.get('value', None)
                if input_value is not None:
                    mtlx_value = self.scalar_to_string(input_value, input_type)
                    if mtlx_value is not None:
                        mtlx_input.setValueString(mtlx_value)
                        mtlx_input.setType(input_type)
                    else:
                        mtlx_input.setValueString(str(input_value))
                else:
                    self.logger.error(f'> Interface input has no value specified: {inputname}')

            # Scan for nodes in the nodegraph
            # - Prelabel nodes
            for node in nodes:
                nodename = node.get(KHR_TEXTURE_PROCEDURALS_NAME, 'node_' + str(node_index))
                if 'name' not in node:
                    node['name'] = nodename
                    node_index += 1

            self.logger.debug(f'> Scan {len(nodes)} nodes')
            for node in nodes:
                nodename = node.get(KHR_TEXTURE_PROCEDURALS_NAME, 'node_' + str(node_index))
                node_type = node.get('nodetype', None)
                output_type = node.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                node_outputs = node.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, [])

                # Check for multiple outputs on the node to use 'multioutput' as the type
                if len(node_outputs) > 1:
                    output_type = MULTI_OUTPUT_TYPE_STRING

                # Create a new node in the graph
                mtlx_node = mtlx_graph.addChildOfCategory(node_type)
                mtlx_node.setName(nodename)
                if output_type:
                    mtlx_node.setType(output_type)
                else:
                    self.logger.error(f'> No output type specified for node: {nodename}')

                # Look for other name, value pair children under node. Such as "xpos": "0.086957",
                # For each add an attribute to the node
                for key, value in node.items():
                    if key not in [KHR_TEXTURE_PROCEDURALS_NAME, 'nodetype', KHR_TEXTURE_PROCEDURALS_TYPE, KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]:
                        self.logger.debug(f'> Add extra node attribute: {key}, {value}')
                        mtlx_node.setAttribute(key, value)

                # Add node inputs
                input_index = 0
                node_inputs = node.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, [])
                for input_item in node_inputs:
                    input_name = input_item.get('name', 'input_' + str(input_index))
                    input_type = input_item.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)

                    # Add node input
                    mtlx_input = mtlx_node.addInput(input_name, input_type)

                    # If input is a file reference, examines textures and images to retrieve the URI
                    if input_type == 'filename':
                        texture_index = input_item.get('texture', None)
                        if texture_index is not None:
                            gltf_textures = gltf_doc.get('textures', None)
                            gltf_images = gltf_doc.get('images', None)
                            if gltf_textures and gltf_images:
                                gltftexture = gltf_textures[texture_index] if texture_index < len(gltf_textures) else None
                                if gltftexture:
                                    uri = self.get_glTF_texture_uri(gltftexture, gltf_images)
                                    mtlx_input.setValueString(uri)

                    # If input has a value, set the value
                    input_value = input_item.get('value', None)
                    if input_value is not None:
                        mtlx_value = self.scalar_to_string(input_value, input_type)
                        if mtlx_value is not None:
                            mtlx_input.setValueString(mtlx_value)
                            mtlx_input.setType(input_type)
                        else:
                            self.logger.error(f'> Unsupported input type: {input_type}. Performing straight assignment.')
                            mtlx_input.setValueString(str(input_value))

                    # Check for connections
                    else:
                        connectable = None

                        # Set any upstream interface input connection
                        if 'input' in input_item:
                            connectable = inputs[input_item[KHR_TEXTURE_PROCEDURALS_INPUT]] if input_item[KHR_TEXTURE_PROCEDURALS_INPUT] < len(inputs) else None
                            mtlx_input.setAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                        
                        # Set any upstream node output connection
                        elif 'output' in input_item:
                            if 'node' in input_item:
                                mtlx_input.setAttribute('output', input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT])
                            else:
                                connectable = outputs[input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT]] if input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT] < len(outputs) else None
                                mtlx_input.setAttribute('output', connectable[KHR_TEXTURE_PROCEDURALS_NAME])

                        # Set and node connection
                        if 'node' in input_item:
                            connectable = nodes[input_item[KHR_TEXTURE_PROCEDURALS_NODE]] if input_item[KHR_TEXTURE_PROCEDURALS_NODE] < len(nodes) else None
                            mtlx_input.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])

                    # Add extra metadata to the input
                    for meta in metadata:
                        if meta in input_item:
                            self.logger.debug(f'> Add extra input attribute: {meta}, {input_item[meta]}')
                            mtlx_input.setAttribute(meta, input_item[meta])

                # TODO CLEANUP: There is no need to add outputs to the node, only to the graph
                output_index = 0
                dump_outputs = False
                if dump_outputs:                
                    for output in node_outputs:
                        output_name = output.get('name', 'output_' + str(output_index))
                        output_type = output.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)

                        connectable = None
                        mtlxoutput = None
                        if 'input' in output:
                            mtlxoutput = mtlx_node.addOutput(output_name, output_type)
                            connectable = inputs[output[KHR_TEXTURE_PROCEDURALS_INPUT]] if output[KHR_TEXTURE_PROCEDURALS_INPUT] < len(inputs) else None
                            mtlxoutput.setAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                        elif 'output' in output:
                            mtlxoutput = mtlx_node.addOutput(output_name, output_type)
                            connectable = outputs[output[KHR_TEXTURE_PROCEDURALS_OUTPUT]] if output[KHR_TEXTURE_PROCEDURALS_OUTPUT] < len(outputs) else None
                            mtlxoutput.setAttribute('output', connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                        elif 'node' in output:
                            mtlxoutput = mtlx_node.addOutput(output_name, output_type)
                            connectable = nodes[output[KHR_TEXTURE_PROCEDURALS_NODE]] if output[KHR_TEXTURE_PROCEDURALS_NODE] < len(nodes) else None
                            mtlxoutput.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                        else:
                            if len(node_outputs) > 1:
                                mtlxoutput = mtlx_node.addOutput(output_name, output_type)

                        if mtlxoutput:
                            # Add extra metadata to the output
                            for key, value in output.items():
                                if key in metadata:
                                    self.logger.debug(f'> Add extra output attribute: {meta}, {input_item[meta]}')
                                    mtlxoutput.setAttribute(key, value)

                # Set node definition string if specified
                if self.add_nodedef_strings:
                    # Add nodedef string to node if desired. Does not work since stdlib is not loaded in.
                    # Nix this ???
                    mtlx_node_def = mtlx_node.getNodeDef()
                    if mtlx_node_def:
                        self.logger.debug(f'> Add nodedef attribute: {mtlx_node_def.getName()}')
                        mtlx_node_def.setAttribute(mx.InterfaceElement.NODE_DEF_ATTRIBUTE, mtlx_node_def.getName())

            # Scan for output interfaces in the nodegraph
            self.logger.debug(f'> Scan {len(outputs)} outputs')
            for output in outputs:
                output_name = output.get('name', 'output_' + str(output_index))
                if 'name' not in output:
                    output['name'] = output_name
                    output_index += 1

                output_type = output.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                mtlx_graph_output = mtlx_graph.addOutput(output_name, output_type)

                connectable = None

                # Check for connection to upstream input
                if 'input' in output:
                    connectable = inputs[output[KHR_TEXTURE_PROCEDURALS_INPUT]] if output[KHR_TEXTURE_PROCEDURALS_INPUT] < len(inputs) else None
                    if connectable:
                        mtlx_graph_output.setAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                    else:
                        self.logger.error(f'Input not found: {output["input"]}, {inputs}')

                # Check for connection to upstream node output                          
                elif 'node' in output:
                    connectable = nodes[output[KHR_TEXTURE_PROCEDURALS_NODE]] if output[KHR_TEXTURE_PROCEDURALS_NODE] < len(nodes) else None
                    if connectable:
                        mtlx_graph_output.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                        if 'output' in output:
                            mtlx_graph_output.setAttribute('output', output[KHR_TEXTURE_PROCEDURALS_OUTPUT])
                    else:
                        self.logger.error(f'> Output node not found: {output["node"]}, {nodes}')

                # Add extra metadata to the output
                for key, value in output.items():
                    if key not in [KHR_TEXTURE_PROCEDURALS_NAME, KHR_TEXTURE_PROCEDURALS_TYPE, 'nodetype', 'node', 'output']:
                        self.logger.debug(f'> Add extra graph output attribute: {key}. Value: {value}')
                        mtlx_graph_output.setAttribute(key, value)

        return root_mtlx

    def gltf_string_to_materialX(self, gltFDocString, stdlib):
        '''
        Convert a glTF document to a MaterialX document.
        @param gltFDocString: The glTF document to import.
        @param stdlib: The MateriaLX standard library to use for the conversion.
        @return The MaterialX document if successful, otherwise None.
        '''
        glTFDoc = json.loads(gltFDocString)
        return self.glTF_to_materialX(glTFDoc, stdlib)

