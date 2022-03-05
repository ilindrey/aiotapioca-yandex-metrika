#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re

with open("README.md", "r", encoding="utf8") as fh:
    readme = fh.read()

package = "async_tapi_yandex_metrika"


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(
        1
    )


setup(
    name="async-tapi-yandex-metrika",
    version=get_version(package),
    description="Python client for API Yandex Metrika",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Pavel Maksimov",
    author_email="vur21@ya.ru",
    url="https://github.com/ilindrey/async-tapi-yandex-metrika",
    packages=[package],
    include_package_data=False,
    install_requires=["aiohttp", "async-tapi-wrapper==0.1.2"],
    extras_require={
        "dev": [
            "black>=22.0",
            "pytest>=7.0",
            "pytest-asyncio>=0.18",
            "aioresponses>=0.7",
        ]
    },
    license="MIT",
    zip_safe=False,
    keywords="tapi,wrapper,yandex,metrika,api,async",
    test_suite="tests",
    package_data={
        package: ["*"],
    },
)
