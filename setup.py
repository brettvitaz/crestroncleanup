from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crestroncleanup',
    version='0.1',
    packages=['crestroncleanup'],
    url='https://github.com/brettvitaz/crestroncleanup',
    license='nunya',
    author='brettvitaz',
    author_email='brett@vitaz.net',
    description='Clean up signal names and other parts of a messy Crestron SIMPL program.',
    long_description=long_description,
    keywords=['crestron', 'simpl', 'cleanup'],
    classifiers=['Development Status :: 3 - Alpha'],
    entry_points={
        'console_scripts': [
            'crestroncleanup = crestroncleanup.crestroncleanup_console:main',
        ]
    }
)
