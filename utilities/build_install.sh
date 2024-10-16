mkdir materialxgltfpt
cp README.md materialxgltfpt
cp README.html materialxgltfpt/index.html
cp -R documents materialxgltfpt/documents
rm -rf source/gltf_materialx_converter/__pycache__
rm -rf source/gltf_materialx_converter.egg-info
cp -R source  materialxgltfpt
rm -rf tests/__pycache__
cp -R tests materialxgltfpt
