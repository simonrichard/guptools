import pip

from setuptools import setup, find_packages

pip.main(["install", "-r", "requirements.txt"])

setup(
    name="guptools",
    version="1.3.0",
    author="Simon Richard",
    author_email="simon.richard@umontreal.ca",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "nltk",
        "python-constraint>=1.3",
        "pyparsing",
    ],
    tests_require=["pytest"],
    package_data={
        "guptools": ["data/*.gup"],
    }
)
