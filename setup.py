from distutils.core import setup
import sys

sys.path.append('obsidian')
import ostart

setup(name='ostart',
    version='0.1',
    author='Adam Lehenbauer',
    description='Start and manage Java processes declaratively',
    package_dir={'': 'obsidian'},
    py_modules=['ostart']
    )
