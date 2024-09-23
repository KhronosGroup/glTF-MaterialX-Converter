
import subprocess

def build():
    try:
        # Run the unit tests
        print("> Running unit tests...")
        cmd = 'python -m unittest discover -s tests -p test_*.py'
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    build()

