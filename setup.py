"""
Active Space Code Generator
"""
import sys
from setuptools import setup, find_packages
import versioneer

short_description = "A Python tool to generate code for active-space coupled-cluster routines".split("\n")[0]

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = None

setup(
    # Self-descriptive entries which should always be present
    name='actgen',
    author='Karthik Gururangan',
    author_email='gururang@msu.edu',
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3-Clause',

    packages=find_packages(),

    include_package_data=True,

    setup_requires=[] + pytest_runner,
)
