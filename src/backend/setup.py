from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='tmr',
        version='0.1.0',
        packages=find_packages(),
        requires=[
            "fastapi",
            "pymongo",
        ]
    )
