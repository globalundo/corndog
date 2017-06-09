import subprocess
from setuptools import setup, find_packages, Extension

setup(
    name='corndog',
    version='0.5',
    author='Oleg Mikhaylov',
    license='GPL',
    packages=['corndog'],
    install_requires=[
        'datadog',
        'multicorn',
    ],
)
