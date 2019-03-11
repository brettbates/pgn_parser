import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgn-parser",
    version="1.0.1",
    author="Brett Bates",
    author_email="b@bmb.io",
    description="PGN Parser is for parsing .pgn chess files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brettbates/pgn_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
    ],
)
