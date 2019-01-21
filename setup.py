import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlmdlu",
    version="0.0.1",
    author="Hossein Parvaneh Gashti",
    author_email="amirhpg.wm@gmail.com",
    description="Download movies for free with your terminal u just need name of it :D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)