import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dmfrbloom",
    version="0.0.6",
    author="Daniel Roberson",
    author_email="daniel@planethacker.net",
    description="Bloom filters with the standard library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/droberson/dmfrbloom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
