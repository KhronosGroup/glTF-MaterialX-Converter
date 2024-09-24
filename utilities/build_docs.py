import subprocess

def build():
        print("> Building docs...")
        subprocess.run("python utilities/replace_string.py -s $TOP -r . utilities/README_template.md -o README.md", shell=True, check=True)
        subprocess.run("python utilities/replace_string.py -rm=True utilities/README_template.md -o documents/README_api.md", shell=True, check=True)
        subprocess.run('pushd documents && doxygen > NUL 2>&1 && popd', shell=True, check=True)
        subprocess.run("python utilities/replace_string.py -s $TOP -r ../.. documents/html/index.html", shell=True, check=True)

if __name__ == "__main__":
    build()
