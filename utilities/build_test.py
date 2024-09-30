
import subprocess

def build():
    try:
        # Run the unit tests
        print("> Running unit tests...")
        cmd = 'python -m unittest discover -s tests -p test_*.py'
        subprocess.run(cmd, check=True)

        print("> Running command line tests...")
        cmd = 'python -m gltf_materialx_converter convert "source/gltf_materialx_converter/data/checkerboard_graph.mtlx" -o "source/gltf_materialx_converter/data/"'
        subprocess.run(cmd, check=True)
        cmd = 'python -m gltf_materialx_converter convert "source/gltf_materialx_converter/data/checkerboard_graph.gltf" -o "source/gltf_materialx_converter/data/"'
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    build()

