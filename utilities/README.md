## Build Utilities

This folder contains a set of utilities to build and generate supporting content for this reposiory:

### Documentation

- `README_template.md` : This is the template README file which is used to generate the top level README.md as well as the version used for API documentation.
- `replace_string.py` : Used as part of the documentation generation process to replace tokens in the template file.

### Build

- `build.sh` : Will pull from head of the repo, install dependencies, and build the package.

- `build_docs.sh` : Will build only the documentation. Called from `build.sh`. Doxygen is assumed to be installed. 

    The README files are generated from the template Markdown file: `utilitites/README_template.md.` 

    This will install the top level as well as the API documentation versions of this file with appropriate formatting to support the `Mermaid` graphs used to node graph diagrams.
- `build_tests.sh` : Will run unit tests as well as command line tests.

`build.sh` is called within the check-in workflow defined in `.github/workflows/main.yml`

### Reference Rendering

- `test_render.py` : Script to render files / folders of MaterialX documents to produce reference images. Uses the path to the `MaterialXView` program specified as an input argument or the  path specified by the environment variable: `MATERIALX_VIEWER`.