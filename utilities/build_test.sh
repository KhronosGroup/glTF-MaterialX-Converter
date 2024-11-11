python -m unittest discover -s tests -p "test_*.py"
python source/gltf_materialx_converter/materialx_to_gltf.py "tests/data/checkerboard_graph.mtlx" -s "tests/schema/schema.json"
python source/gltf_materialx_converter/gltf_to_materialx.py "checkerboard_graph.gltf" --addComments True
rm checkerboard_graph_fromgltf.mtlx checkerboard_graph.gltf

