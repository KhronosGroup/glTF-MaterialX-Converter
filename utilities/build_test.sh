python -m unittest discover -s tests -p "test_*.py"
python -m gltf_materialx_converter gltf "tests/data/checkerboard_graph.mtlx" -s "tests/schema/schema.json"
python -m gltf_materialx_converter mtlx "checkerboard_graph.gltf" --addAssetInfo True
python utilities/mxequivalent.py ./tests/data/add_graph.mtlx ./tests/data/add_graph_fromgltf.mtlx -m -f
python utilities/mxequivalent.py ./tests/data/checkerboard_graph.mtlx ./checkerboard_graph_fromgltf.mtlx -m -f
rm checkerboard_graph_fromgltf.mtlx checkerboard_graph.gltf

