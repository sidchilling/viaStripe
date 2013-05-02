
#from distutils.core import setup
from setuptools import setup, find_packages

#general comment to detect changes in git
#adding a comment to see if git detects a diff...
setup(name = 'potter',
        version = '0.1',
        description = 'Services for PayMe',
        author = 'Siddharth Saha',
        author_email = 'siddharth@shopsocially.com',
	packages = ['potter', 'potter.services', 'potter.conf', 'potter.db', 'potter.conf', 'potter.libs', 'potter.tasks']
		)
