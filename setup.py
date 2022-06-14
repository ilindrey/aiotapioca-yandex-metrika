#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re

with open("README.md", "r", encoding="utf8") as fh:
    readme = fh.read()

package = "aiotapioca_yandex_metrika"

requirements = ["aiohttp>=3.0", "aiotapioca-wrapper>=4.0.1", "orjson>=3.0.0"]
test_requirements = [
    "pytest>=7.0",
    "pytest-asyncio>=0.18",
    "aioresponses>=0.7",
    "async-solipsism>=0.5,<1.0",
]
dev_requirements = [
    *test_requirements,
    "black>=22.0",
    "isort>=5.10.0",
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(
        1
    )


setup(
    name=package,
    version=get_version(package),
    description="Python client for API Yandex Metrika",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Pavel Maksimov, Andrey Ilin",
    author_email="vur21@ya.ru",
    url="https://github.com/ilindrey/aiotapioca-yandex-metrika",
    packages=[package],
    package_dir={package: package},
    include_package_data=False,
    license="MIT",
    zip_safe=False,
    keywords="aiotapioca,wrapper,yandex,metrika,api,async,asyncio",
    python_requires=">=3.7",
    install_requires=requirements,
    test_suite="tests",
    tests_require=test_requirements,
    extras_require={"dev": dev_requirements},
)
