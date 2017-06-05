import pip

from setuptools import setup, find_packages

pip.main(["install", "-r", "requirements.txt"])

setup(
    name="guptools",
    version="1.0.0",
    author="Simon Richard",
    author_email="simon.richard@umontreal.ca",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "python-constraint>=1.3",
        "pyparsing",
    ],
    package_data={
        "guptools": ["data/*.gup"],
    }
)
