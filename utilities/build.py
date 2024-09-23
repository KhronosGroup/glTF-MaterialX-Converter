
import subprocess

def build():
    try:
        # Install the package
        print("> Installing the package...")
        subprocess.run('pip install . -q', check=True)

        # Build the documentation
        subprocess.run('python utilities/build_docs.py', shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    build()

