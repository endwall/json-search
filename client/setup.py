import os

from setuptools import find_packages, setup

src_dir = os.path.dirname(__file__)

def read(filename):
    full_path = os.path.join(src_dir, filename)
    with open(full_path) as fd:
        return fd.read()


if __name__ == "__main__":
    setup(
        name="Json Search Client",
        version="0.1.0",
        author="Yongjun Deng",
        author_email="",
        license="Private",
        url="https://github.com/endwall/json-search",
        description="Json Search Demo",
        long_description=read("README.md"),
        packages=find_packages(),
        test_suite="nose.collector",
    )
