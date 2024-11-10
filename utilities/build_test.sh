python -m unittest discover -s tests -p "test_*.py"
python source/gltf_materialx_converter/materialx_to_gltf.py "tests/data/checkerboard_graph.mtlx" -s "tests/schema/schema.json"
rm checkerboard_graph.gltf

