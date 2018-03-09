# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sample

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
   
    name='translation_augmentation',  
    version=sample.__version__,
    description='A python project that augments sentences using neural machine translation.',
    url='https://github.com/admdemiraj/Text_Augmentation_via_Translation',
    python_requires='>=3',
    author='Admir Demiraj',
    license='MIT',
    author_email='admdemiraj@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    keywords='data_augmentation nlp machine_learning text_augmentation translation',
    scripts = ["runner"],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
   
)
