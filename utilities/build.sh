python -m pip install --upgrade pip
pip install -r requirements.txt
python utilities/replace_string.py -s '$TOP' -r '.' utilities/README_template.md -o README.md
python utilities/replace_string.py -rm=True utilities/README_template.md -o documents/README_api.md
cd documents
doxygen Doxyfile
cd ..
python utilities/replace_string.py -s '$TOP' -r '../..' documents/html/index.html
python -m unittest discover -s tests -p "test_*.py"