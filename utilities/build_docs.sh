pip install .[dev]
python utilities/replace_string.py -s '$TOP' -r '.' utilities/README_template.md -o README.md
python utilities/md2html.py README.md README.html
python utilities/replace_string.py -rm=1 utilities/README_template.md -o documents/README_api.md
cd documents
doxygen Doxyfile
cd ..
python utilities/replace_string.py -s '$TOP' -r '../..' documents/html/index.html
