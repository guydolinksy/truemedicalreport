import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as reqs:
    requirements = reqs.read().splitlines()


with open(os.path.join(os.path.dirname(__file__), 'requirements-ldap.txt'), 'r') as reqs:
    requirements_ldap = reqs.read().splitlines()


if __name__ == '__main__':
    setup(
        name='backend',
        version='0.1.0',
        packages=find_packages(),
        install_requires=requirements,
        extras_require={
            "ldap": requirements_ldap
        }
    )
