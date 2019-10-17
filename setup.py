import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mail-log-parser",
    version="0.0.1",
    author="kinteriq",
    author_email="kinteriq@gmail.com",
    description="Package for parsing mail logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kinteriq/mail-log-parser",
    packages=setuptools.find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)