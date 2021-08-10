import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loadtests",
    version="1.0.0",
    author="HPI Schulcloud",
    author_email="devops@hpi-schul-cloud.de",
    description="Utilities to work with 1password",
    long_description=long_description,
    url="https://github.com/hpi-schul-cloud/load-tests",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
            'bs4==0.0.1',
            'locust==2.0.0',
            'pyyaml==5.4',
            'selenium==3.141.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE V3",
        "Operating System :: OS Independent",
    ],
)
