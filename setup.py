import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="table-tests",
    version="0.0.2",
    author="Egor Urvanov",
    author_email="hedgehogues@bk.ru",
    description="Simple engine for your tests. No code, no noodles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hedgehogues/table-tests",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)