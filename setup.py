import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loadtest",
    version="1.0.0",
    author="HPI Schulcloud",
    author_email="devops@hpi-schul-cloud.de",
    description="Utilities to work with 1password",
    long_description=long_description,
    url="https://github.com/hpi-schul-cloud/loadtests",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE V3",
        "Operating System :: OS Independent",
    ],
)
