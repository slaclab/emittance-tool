from setuptools import setup, find_packages
from os import path, environ

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'requirements.txt'), 'r') as f:
    requirements = f.read().split()


setup(
    name='pyemittance',
    version='v0.1.1',
    author='Philipp Dijkstal',
    author_email='philipp.dijkstal@psi.ch',
    packages=find_packages(),

    package_dir={'emittance-tool':'pyemittance'},
    url='https://github.com/slaclab/emittance-tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.5'
)