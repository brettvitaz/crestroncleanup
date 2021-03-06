from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='crestroncleanup',
    version='0.1',
    packages=['crestroncleanup', 'crestroncleanup.gui_wx'],
    url='https://github.com/brettvitaz/crestroncleanup',
    license='nunya',
    author='brettvitaz',
    author_email='brett@vitaz.net',
    description='Clean up signal names and other parts of a messy Crestron SIMPL Windows program.',
    long_description=long_description,
    keywords=['crestron', 'simpl', 'cleanup'],
    classifiers=['Development Status :: 3 - Alpha'],
    entry_points={
        'console_scripts': [
            'crestroncleanup = crestroncleanup.crestroncleanup_console:main',
        ],
        'gui_scripts': [
            'crestroncleanupgui = crestroncleanup.crestroncleanup_gui:main',
        ]
    }
)
