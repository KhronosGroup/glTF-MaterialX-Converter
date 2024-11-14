## Unit Tests

This folder contains conversion tests scripts as well as test data and a schema file to test validity of glTF Texture Procedural `JSON` content.

### Content

- **test_core.py** :  Script for running core conversion tests.
    This file can be run from the root folder using:
    ```
    python -m unittest tests.test_core
    ```
- **data**: 
    - Each folder contains the following content:
        - input `MaterialX` XML files. 
        - Reference renderings of `MaterialX` files produced using the `utilities\test_render.py` script. Names of image files are the names of the  `MaterialX` file with `.mtlx` replaced with `.png`.
        - `glTF` JSON produced from conversion of `MaterialX` files. Names of JSON files are the names of the  `MaterialX` file with `.mtlx` replaced with `.gltf`.
        - `MaterialX` XML files produced from convertion og `glTF` files. Names of MaterialX files end with
        `_fromgltf.mtlx`.
        - `OpenUSD` files converted from `MaterialX` files if applicable.
        Names of image files are the names of the  `MaterialX` file with `.mtlx` replaced with `.png`.

    - Folder breakdown:
        - The main folder contains test data for basic graph variations, and variations on connectivity to materials 
        - **data/bindings** : Test data dealing with resource bindings such as file textures.
        - **data/gltf_examples** : Test data with variations on glTF Sample files.

- **schema**:
    - JSON schema test data.
    - Note that the `schema.json` file in `tests/schema` is a copy of the official schema being worked on as part of the <a href="https://github.com/KhronosGroup/glTF/tree/KHR_texture_procedurals/extensions/2.0/Khronos/KHR_texture_procedurals">KHR_texture_procedurals</a> specification. 

