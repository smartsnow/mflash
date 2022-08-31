rm -rf dist
python3 -m build
pip3 install -U dist/*.whl --force-reinstall
