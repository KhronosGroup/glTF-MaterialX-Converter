python -m unittest discover -s tests -p "test_*.py"
python source/gltf_materialx_converter/materialx_to_gltf.py "tests/data/checkerboard_graph.mtlx" -s "tests/schema/schema.json"
python source/gltf_materialx_converter/gltf_to_materialx.py "checkerboard_graph.gltf" --addComments True
python utilities/mxequivalent.py ./tests/data/add_graph.mtlx ./tests/data/add_graph_fromgltf.mtlx -m -f
rm checkerboard_graph_fromgltf.mtlx checkerboard_graph.gltf

