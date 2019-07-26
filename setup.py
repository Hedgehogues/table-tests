import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('./requirements.txt')
    
setuptools.setup(
    name="table-test",
    version="0.4.1",
    author="Egor Urvanov",
    author_email="hedgehogues@bk.ru",
    description="Simple engine for your test. No code, no noodles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hedgehogues/table-tests",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_reqs,
)
