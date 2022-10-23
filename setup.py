# -*- coding: utf-8 -*-

import codecs
import os
import re
from setuptools import setup, find_packages


# Method for retrieving the version is taken from the setup.py of pip itself:
# https://github.com/pypa/pip/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cozytouchpy',
    version='replace_by_workflow',
    packages=find_packages(),
    description='Cozytouch python client (fork cozypy)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests>=2'],
    license='GPL-3',
    include_package_data=True,
    url='https://github.com/cyr-ius/cozytouchpy/tree/master',
    author='cyr-ius (forked from biker91620)',
    author_email='cyr-ius@ipocus.net',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Home Automation',
    ],
    keywords=[
        'rest',
        'overkiz',
        'cozytouch',
        'atlantic',
        'thermor',
        'sauter',
        'io',
        'smart-things',
        'iot'
    ],
)
