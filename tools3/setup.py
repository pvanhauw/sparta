#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for leonidas.
"""

import io
import os
import re

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """
    Read file text content.

    :param names: Some path
    :type names: variable length arguments
    :param kwargs: Some option
    :type kwargs: keyworded variable arguments
    :return: file content
    :rtype: stream
    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """
    Find version string.

    :param file_paths: Some paths
    :type file_paths: path-like objects
    :return: version string.
    :rtype: string
    :raises RuntimeError: Unable to find version string

    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("requirements.txt", "r") as fh:
    dependencies = [l.strip() for l in fh]


long_description = read("README.rst")


tests_require = []


setup(
    name="leonidas",
    version=find_version("leonidas", "__init__.py"),
    description="post processing tools fopr sparta",
    long_description=long_description,
    author="P.V.H.",
    license="",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "tasks"]),
    package_data={
        'leonidas': [
            'data/MCR/*.mcr',
        ]
    },
    data_files=['requirements.txt'],
    entry_points={
        "console_scripts": [
            "pv2sparta = leonidas.pv2sparta:main",
            "log2csv = leonidas.pizza.olog:main",
        ]
    },
    tests_require=tests_require,
    install_requires=dependencies,
    zip_safe=False,
    python_requires=">=3.8",
    extras_require={"testing": tests_require},
)
# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
