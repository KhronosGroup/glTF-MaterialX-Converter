## MaterialX / glTF Procedurals Interop

[![Build Status](https://github.com/KhronosGroup/glTF-MaterialX-Converter/workflows/main/badge.svg)](https://github.com/KhronosGroup/glTF-MaterialX-Converter/actions?query=branch%3Amain)

### Introduction

This package supports the bi-directional translation between MaterialX material graphs and the glTF Procedural Textures extension.

- The Khronos extensions can be found here:
  - <a href="https://github.com/KhronosGroup/glTF/tree/KHR_texture_procedurals/extensions/2.0/Khronos/KHR_texture_procedurals">KHR_texture_procedurals</a>
  - <a href="https://github.com/KhronosGroup/glTF/tree/KHR_texture_procedurals/extensions/2.0/Vendor/EXT_texture_procedurals_mx_1_39">EXT_texture_procedurals_mx_1_39</a>
- The MaterialX specification documents can be found <a href="https://github.com/AcademySoftwareFoundation/MaterialX/tree/main/documents/Specification">here</a>

### Dependencies

- The 1.39 release (or patch releases) of MaterialX available on 
<a href="https://pypi.org/project/MaterialX/">PyPi</a> is required.
- The <code>jsonschema</code> package if Schema validation is desired

### Setup

The Github repository can be forked / cloned locally and the package built using `pip` as follows from the root folder:

`pip install .`

All dependencies listed will be installed if required. 

#### Command Line Interface

Command line documentation forthcoming.

### Documentation

#### API

API documentation forthcoming.

### Unit Tests

Unit test information forthcoming. 

#### Sample Data

The following is some sample data data which shows MaterialX XML document, the corresponding glTF JSON, and a reference rendering using the `MaterialXViewer` sample application which comes as part of the MaterialX distribution.  

<table>
<tr>
<th>Description
<th>Documents
<th>Reference Image

<tr>
<td>The following is a pattern graph that produces a checkerboard pattern. 

The two input colors, and a texture coordinate tiling option are exposed on the node graph. The output is a color which is routed to a downstream glTF PBR shading node (glTF material).

```mermaid
graph TB
    subgraph NG_main
    NG_main_uvtiling([uvtiling:8,8])
    style NG_main_uvtiling  fill:#09D, color:#FFF
    NG_main_color1([color1:1,0.094118,0.031373])
    style NG_main_color1  fill:#09D, color:#FFF
    NG_main_color2([color2:0.035294,0.090196,0.878431])
    style NG_main_color2  fill:#09D, color:#FFF
    NG_main_output_N_mtlxmix_out([output_N_mtlxmix_out])
    style NG_main_output_N_mtlxmix_out  fill:#09D, color:#FFF
    NG_main_N_mtlxmix[N_mtlxmix]
    NG_main_N_mtlxdotproduct[N_mtlxdotproduct]
    NG_main_N_mtlxmult[N_mtlxmult]
    NG_main_N_mtlxsubtract[N_mtlxsubtract]
    NG_main_N_mtlxfloor[N_mtlxfloor]
    NG_main_N_modulo[N_modulo]
    NG_main_Texcoord[Texcoord:0]
    end
    Gltf_pbr[Gltf_pbr]
    MAT_Gltf_pbr([MAT_Gltf_pbr])
    style MAT_Gltf_pbr   fill:#090, color:#FFF
    NG_main_N_mtlxmix --> NG_main_output_N_mtlxmix_out
    NG_main_color1 --"fg"--> NG_main_N_mtlxmix
    NG_main_color2 --"bg"--> NG_main_N_mtlxmix
    NG_main_N_modulo --"mix"--> NG_main_N_mtlxmix
    NG_main_N_mtlxfloor --"in1"--> NG_main_N_mtlxdotproduct
    NG_main_Texcoord --"in1"--> NG_main_N_mtlxmult
    NG_main_uvtiling --"in2"--> NG_main_N_mtlxmult
    NG_main_N_mtlxmult --"in1"--> NG_main_N_mtlxsubtract
    NG_main_N_mtlxsubtract --"in"--> NG_main_N_mtlxfloor
    NG_main_N_mtlxdotproduct --"in1"--> NG_main_N_modulo
    NG_main_output_N_mtlxmix_out --"base_color"--> Gltf_pbr
    Gltf_pbr --"surfaceshader"--> MAT_Gltf_pbr
```
</td>
<td>
<a href="./tests/data/checkerboard_graph.mtlx">MTLX</a>
<a href="./tests/data/checkerboard_graph.gltf">GLTF</a>
</td>
<td><img src="./tests/data/checkerboard_graph.png">
</td>
</tr>

</table>
