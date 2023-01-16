
# Tested on Python 3.9.0

run:
	py main.py

install:
	python -m pip install -r requirements.txt

installed:
	python -m pip list

unittest: tests/
	 python -m unittest discover . "*_test.py"

coverage: tests/
	coverage run -m --omit=*test_integration.py,*__init__.py,*\site-packages\*.py,*mainview.py,*\fileops.py,*mainpresenter.py unittest discover . "*_test.py" 
	coverage html
	coverage report -m

# Run pylint for 'main' and 'tests' modules
# Diable W0212: Access to a protected member

pylint:
	pylint tests main --disable=W0212 --ignore=fileops_test.py

flake8:
	flake8 --exclude  __init__.py
