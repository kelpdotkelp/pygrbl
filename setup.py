from setuptools import setup

with open('./README.md', 'r') as file:
    long_description = file.read()

setup(
    name='pygrbl',
    version='1.0.1',
    description='A simple interface for controlling cartesian robots with GRBL.',
    packages=['pygrbl'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kelpdotkelp/pygrbl',
    author='kelpdotkelp')