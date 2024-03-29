import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as src:
    requirements = src.read().splitlines()

if __name__ == '__main__':
    setup(
        name='tmr_sheba_faker',
        version='0.1.0',
        packages=find_packages(),
        install_requires=requirements
    )
