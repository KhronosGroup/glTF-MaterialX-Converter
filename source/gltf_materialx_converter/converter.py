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
#  @brief Default name for a MaterialX material for generation.
MTLX_DEFAULT_MATERIAL_NAME = 'MATERIAL_0'

## @var MTLX_MATERIAL_PREFIX
#  @brief Prefix for MaterialX material name for generation.
MTLX_MATERIAL_PREFIX = 'MATERIAL_'

## @var MTLX_DEFAULT_SHADER_NAME
#  @brief Default name for a MaterialX shader for generation.
MTLX_DEFAULT_SHADER_NAME = 'SHADER_0'

## @var MTLX_NODEGRAPH_NAME_ATTRIBUTE
#  @brief Attribute for nodegraph references in MaterialX.
MTLX_NODEGRAPH_NAME_ATTRIBUTE = 'nodegraph'

## @var MTLX_DEFAULT_NODE_NAME
#  @brief Default name for a MaterialX graph nodes for generation.
MTLX_DEFAULT_NODE_NAME = 'NODE_0'

## @var MTLX_DEFAULT_INPUT_NAME
#  @brief Default name for a MaterialX graph nodes for generation.
MTLX_DEFAULT_INPUT_NAME = 'INPUT_0'

## @var MTLX_DEFAULT_OUTPUT_NAME
#  @brief Default name for a MaterialX graph nodes for generation.
MTLX_DEFAULT_OUTPUT_NAME = 'OUTPUT_0'

## @var MTLX_DEFAULT_GRAPH_NAME
#  @brief Default name for a MaterialX node graphs for generation.
MTLX_DEFAULT_GRAPH_NAME = 'GRAPH_0'

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

        - add_asset_info : bool
            - Option to add asset information during the conversion to MaterialX.
                
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
        self.add_asset_info = False

        # Options for conversion from Materialx
        self.supported_types = ['boolean', 'string', 'integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_scalar_types = ['integer', 'matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'float', 'color3', 'color4']
        self.supported_array_types = ['matrix33', 'matrix44', 'vector2', 'vector3', 'vector4', 'color3', 'color4']
        self.standard_ui_metadata = ['xpos', 'ypos', 'width', 'height', 'uicolor']
        self.supported_metadata = ['colorspace', 'unit', 'unittype', 
                                   'uiname', 'uimin', 'uimax', 'uisoftmin', 'uisoftmax', 'uistep', 'uifolder', 'uiadvanced', 'uivisible',
                                   'defaultgeomprop', 'uniform', 
                                   'doc'] + self.standard_ui_metadata
        self.supported_graph_metadata = ['colorspace', 'unit', 'unittype', 'uiname', 'doc'] + self.standard_ui_metadata

    def set_debug(self, debug):
        '''
        Set the debug flag for the converter.
        @param debug: The debug flag.
        '''
        if debug:
            self.logger.setLevel(lg.DEBUG)
        else:
            self.logger.setLevel(lg.INFO)

    def get_standard_ui_metadata(self):
        '''
        Get the standard UI metadata defined by MaterialX.
        @return The standard UI metadata.
        '''
        return self.standard_ui_metadata

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
    
    def get_graph_metadata(self):
        '''
        Get the supported graph metadata for the converter.
        @return The metadata.
        '''
        return self.supported_graph_metadata

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
                    return_value = [ int(value) ]
                else:
                    return_value = [ float(value) ]
    
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
        nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK] = {}
        nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK] = {}
        nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK] = []
        procs.append(nodegraph)

        metadata = self.get_metadata()

        # Set nodegraph metadata
        graph_metadata = self.get_graph_metadata()
        for meta in graph_metadata:
            if graph.getAttribute(meta):
                nodegraph[meta] = graph.getAttribute(meta)

        # Add nodes to to dictonary. Use path as this is globally unique
        #
        for node in graph.getNodes():
            json_node = {'name': node.getNamePath() if use_paths else node.getName()}
            nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK].append(json_node)
            nodegraph_nodes[node.getNamePath()] = len(nodegraph[KHR_TEXTURE_PROCEDURALS_NODES_BLOCK]) - 1

        # Add inputs to the graph
        #
        for input in graph.getInputs():
            input_name = input.getNamePath() if use_paths else input.getName()
            json_node = {
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
                nodegraph[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK][input_name] = json_node

                # Add input to dictionary
                nodegraph_inputs[input.getNamePath()] = input_name
            else:
                self.logger.error(f'> No value or invalid connection specified for input. Input skipped: {input.getNamePath()}')

        # Add outputs to the graph
        #
        for output in graph_outputs:
            for output in graph_outputs:
                output_name = output.getNamePath() if use_paths else output.getName()
                json_node = {}
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

                nodegraph[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK][output_name] = json_node                    

                # Add output to dictionary
                nodegraph_outputs[output.getNamePath()] = output_name

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
            inputs = {}
            for input in node.getInputs():
                input_name = input.getNamePath() if use_paths else input.getName()
                input_item = {
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
                            input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_string
                            #connected_node_outputs = connection_node.getOutputs()
                            #for i, connected_output in enumerate(connected_node_outputs):
                            #    if connected_output.getName() == output_string:
                            #        input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT] = i
                            #        break
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

                inputs[input_name] = input_item

            # Add node inputs list
            if inputs:
                json_node[KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK] = inputs

            # Find explicit node outputs
            outputs = {}
            for output in node.getOutputs():
                output_name = output.getName()
                output_item = {
                    'nodetype': KHR_TEXTURE_PROCEDURALS_OUTPUT,
                    KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                }
                outputs[output_name] = output_item

            # Add implicit outputs (based on nodedef)
            if nodedef:
                for output in nodedef.getOutputs():
                    if not any(output_item != output.getName() for output_item in outputs):
                        output_item = {
                            'nodetype': KHR_TEXTURE_PROCEDURALS_OUTPUT,
                            KHR_TEXTURE_PROCEDURALS_TYPE: output.getType()
                        }
                        outputs[output.getName()] = output_item
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
            # Note that this ordering must match the order of the inputs in the MaterialX shader
            # in order produce an instance which matches the definition.
            ['base_color', 'baseColorTexture', 'pbrMetallicRoughness'],
            ['metallic', 'metallicRoughnessTexture', 'pbrMetallicRoughness'],
            ['roughness', 'metallicRoughnessTexture', 'pbrMetallicRoughness'],
            ['normal', 'normalTexture', ''],
            ['occlusion', 'occlusionTexture', ''],
            ['emissive', 'emissiveTexture', '']
        ]
        input_maps[MTLX_UNLIT_CATEGORY_STRING] = [['emission_color', 'baseColorTexture', 'pbrMetallicRoughness']]

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
                is_unlit = (category == MTLX_UNLIT_CATEGORY_STRING)

                if (is_pbr or is_unlit) and pbr_nodes.get(path) is None:
                    # Add fallback if not already added
                    if fallback_texture_index == -1:
                        fallback_texture_index = self.add_fallback_texture(json_data, fallback_image_data)

                    self.logger.info(f'> Convert shader to glTF: {shader_node.getNamePath()}. Category: {category}')
                    pbr_nodes[path] = shader_node

                    material = {}

                    material[KHR_TEXTURE_PROCEDURALS_NAME] = path
                    if is_unlit:
                        material[KHR_EXTENSIONS_BLOCK] = {}
                        material[KHR_EXTENSIONS_BLOCK][KHR_MATERIALX_UNLIT] = {}
                        # Append if not found
                        if KHR_MATERIALX_UNLIT not in extensions_used:
                            extensions_used.append(KHR_MATERIALX_UNLIT)

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
                        output_name = ""
                        outputs_length = 0
                        if procs:
                            for i, proc in enumerate(procs):
                                if proc[KHR_TEXTURE_PROCEDURALS_NAME] == nodegraph_name:
                                    graph_index = i
                                    outputs_length = len(nodegraph_output) 
                                    if  outputs_length > 0:
                                        outputs_list = proc[KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]
                                        for test_name, item in outputs_list.items():
                                            if test_name == nodegraph_output:
                                                output_name = test_name
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
                            if len(output_name):
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_name
                        
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
                            output_name = ""

                            # Assign an output index if the graph has more than one output
                            if len(nodegraph_output) > 0:
                                nodegraph_outputPath = f"{nodegraph_name}/{nodegraph_output}"
                                if nodegraph_outputPath in output_nodes:
                                    output_name = output_nodes[nodegraph_outputPath]
                                    lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = output_name
                                else:
                                    self.logger.error(f'> Failed to find output: {nodegraph_output} '
                                                      ' in: {output_nodes}')
                            else:
                                # Set to first key in output_nodes
                                lookup[KHR_TEXTURE_PROCEDURALS_OUTPUT] = next(iter(output_nodes.values()))

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

    def set_add_asset_info(self, add_asset_info):
        '''
        Set the flag to add asset information from glTF to the generated MaterialX files.
        @param add_asset_info: The flag to add asset information
        '''
        self.add_asset_info = add_asset_info
        
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
            elif type in ['integer', 'float']: 
                # If it'of type 'float' or 'integer', extract value from array
                return_value = '{0:g}'.format(value[0]) if isinstance(value, list) else '{0:g}'.format(value) if isinstance(value, float) else str(value)                
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

    def have_procedural_tex_extensions(self, gltf_doc):
        '''
        Does the glTF document have the required procedural texture extensions.
        
        @param gltf_doc: The glTF document to check.
        @return The result of the check in the form [boolean, string], where "boolean" is true if the extensions are present,
                 and "string" is an error message if the extensions are not present.
        '''
        # Check extensionsUsed for KHR_texture_procedurals
        extensions_used = gltf_doc.get('extensionsUsed', None)
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

    def glTF_to_materialX(self, gltf_doc, stdlib):
        '''
        Convert a glTF document to a MaterialX document.
        @param gltFDoc: The glTF document to import.
        @param stdlib: The MateriaLX standard library to use for the conversion.
        @return The MaterialX document if successful, otherwise None.
        '''
        if not gltf_doc:
            self.logger.error('> No glTF document specified')
            return None

        extension_check = self.have_procedural_tex_extensions(gltf_doc)
        if extension_check[0] is None:
            return None

        # Prepare the glTF to add names to the graph if not already present
        self.glTF_graph_create_names(gltf_doc)

        doc = mx.createDocument()
        doc.setAttribute('colorspace', 'lin_rec709')

        # Import the graph
        self.glTF_graph_to_materialX(doc, gltf_doc)

        global_extensions = gltf_doc.get('extensions', None)
        procedurals = None
        if global_extensions and KHR_TEXTURE_PROCEDURALS in global_extensions:
            procedurals = global_extensions[KHR_TEXTURE_PROCEDURALS].get(KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK, None)
            #self.logger.debug(f'Imported all procedurals: {procedurals}')

        # Import materials and connect to graphs as needed
        gltf_materials = gltf_doc.get(KHR_MATERIALS_BLOCK, None)
        if gltf_materials:

            input_maps = {}
            input_maps[MTLX_GLTF_PBR_CATEGORY] = [
                ['base_color', 'baseColorTexture', 'pbrMetallicRoughness'],
                ['metallic', 'metallicRoughnessTexture', 'pbrMetallicRoughness'],
                ['roughness', 'metallicRoughnessTexture', 'pbrMetallicRoughness'],
                ['occlusion', 'occlusionTexture', ''],
                ['normal', 'normalTexture', ''],
                ['emissive', 'emissiveTexture', '']
            ]
            input_maps[MTLX_UNLIT_CATEGORY_STRING] = [['emission_color', 'baseColorTexture', 'pbrMetallicRoughness']]

            for gltf_material in gltf_materials:

                mtlx_shader_name = gltf_material.get(KHR_TEXTURE_PROCEDURALS_NAME, MTLX_DEFAULT_SHADER_NAME)
                mtlx_material_name = ''
                if len(mtlx_shader_name) == 0:
                    mtlx_shader_name = MTLX_DEFAULT_SHADER_NAME
                    mtlx_material_name = MTLX_DEFAULT_MATERIAL_NAME
                else:
                    mtlx_material_name = MTLX_MATERIAL_PREFIX + mtlx_shader_name
                
                mtlx_shader_name = doc.createValidChildName(mtlx_shader_name)
                mtlx_material_name = doc.createValidChildName(mtlx_material_name)

                use_unlit = False
                extensions = gltf_material.get('extensions', None)
                if extensions and KHR_MATERIALX_UNLIT in extensions:
                    use_unlit = True

                shader_category = MTLX_GLTF_PBR_CATEGORY
                #nodedef_string = 'ND_gltf_pbr_surfaceshader'
                if use_unlit:
                    shader_category = MTLX_UNLIT_CATEGORY_STRING
                    nodedef_string = 'ND_surface_unlit'
                
                shader_node = doc.addNode(shader_category, mtlx_shader_name, mx.SURFACE_SHADER_TYPE_STRING)                
                
                # No need to add all inputs from nodedef.
                # In fact if there is a defaultgeomprop then it will be added automatically
                # without any value or connection which causes a validation error.
                #if stdlib:
                    #odedef = stdlib.getNodeDef(nodedef_string)
                    #if nodedef:
                    #    self.add_inputs_from_nodedef(shader_node, nodedef)

                if procedurals:
                    current_map = input_maps[shader_category]
                    for map_item in current_map:
                        dest_input = map_item[0]
                        source_texture = map_item[1]
                        source_parent = map_item[2]
        
                        if source_parent:
                            if source_parent == 'pbrMetallicRoughness':
                                if 'pbrMetallicRoughness' in gltf_material:
                                    source_texture = gltf_material['pbrMetallicRoughness'].get(source_texture, None)
                                else:
                                    source_texture = None
                        else:
                            source_texture = gltf_material.get(source_texture, None)

                        base_color_texture = source_texture

                        if base_color_texture:
                            extensions = base_color_texture.get('extensions', None)
                            if extensions and KHR_TEXTURE_PROCEDURALS in extensions:
                                KHR_texture_procedurals = extensions[KHR_TEXTURE_PROCEDURALS]
                                procedural_index = KHR_texture_procedurals.get('index', None)
                                output = KHR_texture_procedurals.get('output', None)
                                
                                if procedural_index is not None and procedural_index < len(procedurals):
                                    proc = procedurals[procedural_index]
                                    if proc:
                                        nodegraph_name = proc.get('name')
                                        graph_outputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, None)
                                        output_count = len(graph_outputs)
                                        if graph_outputs:
                                            if output is not None:
                                                proc_output = None
                                                for key, value in graph_outputs.items():
                                                    if key == output:
                                                        proc_output = value
                                                        break
                                            
                                            if proc_output:
                                                input_node = shader_node.getInput(dest_input)
                                                if not input_node:
                                                    input_node = shader_node.addInput(dest_input, proc_output[KHR_TEXTURE_PROCEDURALS_TYPE])
                                                
                                                if input_node:
                                                    input_node.removeAttribute('value')
                                                    input_node.setNodeGraphString(nodegraph_name)
                                                    if output_count > 1:
                                                        input_node.setAttribute('output', proc_output[KHR_TEXTURE_PROCEDURALS_NAME])


                material_node = doc.addNode(mx.SURFACE_MATERIAL_NODE_STRING, mtlx_material_name, mx.MATERIAL_TYPE_STRING)
                shader_input = material_node.addInput(mx.SURFACE_SHADER_TYPE_STRING, mx.SURFACE_SHADER_TYPE_STRING)
                shader_input.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, mtlx_shader_name)

                self.logger.info(f'> Import material: {material_node.getName()}. Shader: {shader_node.getName()}')

        # Import asset information as a doc string
        if self.add_asset_info:
            asset = gltf_doc.get('asset', None)
            mtlx_doc_string = ''
            if asset:
                version = asset.get('version', None)
                if version:
                    mtlx_doc_string += f'glTF version: {version}. '

                generator = asset.get('generator', None)
                if generator:
                    mtlx_doc_string += f'glTF generator: {generator}. '

                copyRight = asset.get('copyright', None)
                if copyRight:
                    mtlx_doc_string += f'Copyright: {copyRight}. '

                if mtlx_doc_string:
                    doc.setDocString(mtlx_doc_string)

        return doc      
    
    def glTF_graph_clear_names(self, gltf_doc):
        '''
        Clear all the names for all procedural graphs and materials
        @param gltf_doc: The glTF document to clear the names in.
        '''
        extensions = gltf_doc.get('extensions', None)
        procedurals = None
        if extensions:
            procedurals = extensions.get(KHR_TEXTURE_PROCEDURALS, {}).get(KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK, None)

        if procedurals:
            for proc in procedurals:
                # Remove the name from the procedural graph
                proc.pop(KHR_TEXTURE_PROCEDURALS_NAME, None)

                inputs = proc.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, {})
                outputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, {})
                nodes = proc.get(KHR_TEXTURE_PROCEDURALS_NODES_BLOCK, [])

                # Cannot clear key names
                #for input_item in inputs:
                #    input_item.pop(KHR_TEXTURE_PROCEDURALS_NAME, None)
                #for output_item in outputs:
                #    output_item.pop(KHR_TEXTURE_PROCEDURALS_NAME, None)
                for node in nodes:
                    node.pop(KHR_TEXTURE_PROCEDURALS_NAME, None) 

        materials = gltf_doc.get(KHR_MATERIALS_BLOCK, None)
        if materials:
            for material in materials:
                material.pop(KHR_TEXTURE_PROCEDURALS_NAME, None)

    def glTF_graph_create_names(self, gltf_doc):
        '''
        Create names for all procedural graphs and materials if they don't already exist.
        This method should always be run before converting a glTF document to MaterialX to
        ensure that all connection references to elements are also handled. 
        @param gltf_doc: The glTF document to clear the names in.
        '''
        # Use a dummy document to handle unique name generation
        dummy_doc = mx.createDocument()

        extensions = gltf_doc.get('extensions', None)
        procedurals = None
        if extensions:
            procedurals = extensions.get(KHR_TEXTURE_PROCEDURALS, {}).get(KHR_TEXTURE_PROCEDURALS_PROCEDURALS_BLOCK, None)

        if procedurals:
            # Scan all procedurals
            for proc in procedurals:
                # Generate a procedural graph name if not already set
                proc_name = proc.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                if len(proc_name) == 0:
                    proc_name = MTLX_DEFAULT_GRAPH_NAME
                proc['name'] = dummy_doc.createValidChildName(proc_name)
                #self.logger.info('Add procedural:' + proc['name'])
                dummy_graph = dummy_doc.addNodeGraph(proc['name'])                    
                
                inputs = proc.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, {})
                outputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, {})
                nodes = proc.get(KHR_TEXTURE_PROCEDURALS_NODES_BLOCK, [])

                # Generate input names if not already set
                if 0:
                    for input_item in inputs:
                        input_name = input_item.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                        if len(input_name) == 0:
                            input_name = MTLX_DEFAULT_INPUT_NAME
                        input_item['name'] = dummy_graph.createValidChildName(input_name)
                        self.logger.debug('Add input:' + input_item['name'])
                        dummy_graph.addInput(input_item['name'])

                    # Generate output names if not already set
                    for output_item in outputs:
                        output_name = output_item.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                        if len(output_name) == 0:
                            output_name = MTLX_DEFAULT_OUTPUT_NAME
                        output_item['name'] = dummy_graph.createValidChildName(output_name)
                        self.logger.debug('Add output:' + output_item['name'])
                        dummy_graph.addOutput(output_item['name'])

                # Generate node names if not already set
                for node in nodes:
                    node_name = node.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                    if len(node_name) == 0:
                        node_name = MTLX_DEFAULT_NODE_NAME
                    node['name'] = dummy_graph.createValidChildName(node_name)
                    #self.logger.info('Add node:' + node['name'])
                    node_type = node.get('nodetype', None)
                    dummy_graph.addChildOfCategory(node_type, node['name'])

        # Generate shader names.
        materials = gltf_doc.get(KHR_MATERIALS_BLOCK, None)
        if materials:
            for material in materials:
                material_name = material.get(KHR_TEXTURE_PROCEDURALS_NAME, '')
                if len(material_name) == 0:
                    material_name = MTLX_DEFAULT_SHADER_NAME
                material['name'] = dummy_doc.createValidChildName(material_name)
                dummy_doc.addNode(MTLX_GLTF_PBR_CATEGORY, material['name'], mx.SURFACE_SHADER_TYPE_STRING)                                
    
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

            # Assign a name to the graph if not already set
            graph_name = proc.get('name', 'GRAPH_' + str(graph_index))
            if len(graph_name) == 0:
                graph_name = 'GRAPH_' + str(graph_index)
            graph_name = doc.createValidChildName(graph_name)
            proc['name']  = graph_name
            
            # Create new nodegraph and add metadata
            self.logger.info(f'> Create new nodegraph: {graph_name}')
            mtlx_graph = doc.addNodeGraph(graph_name)
            graph_metadata= self.get_graph_metadata()
            for meta in graph_metadata:
                if meta in proc:
                    proc_meta_data = proc[meta]
                    self.logger.debug(f'> Add extra graph attribute: {meta}, {proc_meta_data}')
                    mtlx_graph.setAttribute(meta, proc_meta_data)

            root_mtlx = mtlx_graph

            inputs = proc.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, {})
            outputs = proc.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, {})
            nodes = proc.get(KHR_TEXTURE_PROCEDURALS_NODES_BLOCK, [])

            # - Prelabel nodes
            # Pre-label inputs
            for input_name, input_item in inputs.items():
                if len(input_name) == 0:
                    input_name = MTLX_DEFAULT_INPUT_NAME
                input_item['name'] = mtlx_graph.createValidChildName(input_name)
                if len(input_name) == 0:
                    input_name = MTLX_DEFAULT_INPUT_NAME
                input_item['name'] = mtlx_graph.createValidChildName(input_name)
            for output_name, output_item in outputs.items():
                if len(output_name) == 0:
                    output_name = MTLX_DEFAULT_OUTPUT_NAME
                output_item['name'] = mtlx_graph.createValidChildName(output_name)
            for node in nodes:
                node_name = node.get(KHR_TEXTURE_PROCEDURALS_NAME, MTLX_DEFAULT_NODE_NAME)
                if len(node_name) == 0:
                    node_name = MTLX_DEFAULT_NODE_NAME
                node['name'] = mtlx_graph.createValidChildName(node_name)            

            # Scan for input interfaces in the node graph
            self.logger.debug(f'> Scan {len(inputs)} inputs')
            for inputname, input_item in inputs.items():
                #inputname = input_item.get('name', None)

                # A type is required
                input_type = input_item.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                if not input_type:
                    self.logger.error(f'> Input type not found for graph input: {inputname}')
                    continue

                # Add new interface input
                mtlx_input = mtlx_graph.addInput(inputname, input_type)
                # Add extra metadata to the input
                for meta in metadata:
                    if meta in input_item:
                        self.logger.debug(f'> Add extra interface attribute: {meta}, {input_item[meta]}')
                        mtlx_input.setAttribute(meta, input_item[meta])

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
            self.logger.debug(f'> Scan {len(nodes)} nodes')
            for node in nodes:
                node_name = node.get(KHR_TEXTURE_PROCEDURALS_NAME, None)
                node_type = node.get('nodetype', None)
                output_type = node.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                node_outputs = node.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, [])

                # Create a new node in the graph
                mtlx_node = mtlx_graph.addChildOfCategory(node_type, node_name)

                # Check for multiple outputs on the node to use 'multioutput'
                if len(node_outputs) > 1:
                    output_type = MULTI_OUTPUT_TYPE_STRING
                    #mtlx_node.setType(output_type)

                if output_type:
                    mtlx_node.setType(output_type)
                else:
                    self.logger.error(f'> No output type specified for node: {node_name}')

                # Look for other name, value pair children under node. Such as "xpos": "0.086957",
                # For each add an attribute to the node
                for key, value in node.items():
                    if key not in [KHR_TEXTURE_PROCEDURALS_NAME, 'nodetype', KHR_TEXTURE_PROCEDURALS_TYPE, KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK]:
                        self.logger.debug(f'> Add extra node attribute: {key}, {value}')
                        mtlx_node.setAttribute(key, value)

                # Add node inputs
                node_inputs = node.get(KHR_TEXTURE_PROCEDURALS_INPUTS_BLOCK, {})
                for input_name, input_item in node_inputs.items():
                    if not input_name:
                        input_name = MTLX_DEFAULT_INPUT_NAME
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
                            # Get 'input' value
                            input_key = input_item['input']
                            if input_key in inputs:
                                connectable = inputs[input_key]
                                mtlx_input.setAttribute(MTLX_INTERFACEINPUT_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])
                            else:
                                self.logger.error(f'Input key not found: {input_key}')
                        
                        # Set any upstream node output connection
                        elif 'output' in input_item:
                            if 'node' not in input_item:
                                connectable = outputs[input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT]] if input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT] < len(outputs) else None
                                mtlx_input.setAttribute('output', connectable[KHR_TEXTURE_PROCEDURALS_NAME])

                        # Set and node connection
                        if 'node' in input_item:
                            connectable = nodes[input_item[KHR_TEXTURE_PROCEDURALS_NODE]] if input_item[KHR_TEXTURE_PROCEDURALS_NODE] < len(nodes) else None
                            mtlx_input.setAttribute(MTLX_NODE_NAME_ATTRIBUTE, connectable[KHR_TEXTURE_PROCEDURALS_NAME])

                            if 'output' in input_item:
                                # Get the node to connect to
                                connectable = nodes[input_item[KHR_TEXTURE_PROCEDURALS_NODE]] if input_item[KHR_TEXTURE_PROCEDURALS_NODE] < len(nodes) else None
                                if connectable:
                                    # Get the output name to connect to
                                    #connected_outputs = connectable.get(KHR_TEXTURE_PROCEDURALS_OUTPUTS_BLOCK, {})
                                    #if connected_outputs:
                                    #    output_name = list(connected_outputs.keys())[list(connected_outputs.values()).index(output)]
                                    #    print(">>> Scan connected outputs:", connected_outputs, "for output:", output_name)
                                    #    output_string = connected_outputs.get(output_name, "")
                                    mtlx_input.setAttribute('output', input_item['output'])
                                    self.logger.debug(f'Set output specifier on input: {mtlx_input.getNamePath()}. Value: {input_item[KHR_TEXTURE_PROCEDURALS_OUTPUT]}')

                    # Add extra metadata to the input
                    for meta in metadata:
                        if meta in input_item:
                            self.logger.debug(f'> Add extra input attribute: {meta}, {input_item[meta]}')
                            mtlx_input.setAttribute(meta, input_item[meta])

                # Add outputs for multioutput nodes
                if len(node_outputs) > 1:
                    for output_name, output in node_outputs.items():
                        output_type = output.get(KHR_TEXTURE_PROCEDURALS_TYPE, None)
                        mtlxoutput = mtlx_node.addOutput(output_name, output_type)
                        self.logger.debug(f'Add multioutput output {mtlxoutput.getNamePath()} of type {output_type} to node {node_name}')



            # Scan for output interfaces in the nodegraph
            self.logger.info(f'> Scan {len(outputs)} procedural outputs')
            for output_name, output in outputs.items():
                #output_name = output.get('name', None)
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
        gltf_doc = json.loads(gltFDocString)
        return self.glTF_to_materialX(gltf_doc, stdlib)

