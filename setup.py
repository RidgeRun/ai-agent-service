# Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
# All Rights Reserved.
#
# The contents of this software are proprietary and confidential to RidgeRun,
# LLC.  No part of this program may be photocopied, reproduced or translated
# into another programming language without prior written consent of
# RidgeRun, LLC.  The user is free to modify the source code after obtaining
# a software license from RidgeRun.  All source code changes must be provided
# back to RidgeRun without any encumbrance.

# Install with: python3 -m pip install .
# For developer mode install with: pip install -e .

# pylint: skip-file

import logging
import shlex
from subprocess import check_call

import setuptools
from setuptools.command.develop import develop

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ai-agent",
    version="1.0.1",
    author='RidgeRun LLC',
    author_email='support@ridgerun.com',
    description="RidgeRun AI Agent Microservice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://ridgerun.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.0, <4',
    install_requires=[
        'pydantic',
        'flask',
        'flask-cors',
        'sphinx',
        'sphinx_rtd_theme',
        'sphinx-mdinclude'
    ],
    entry_points={
        'console_scripts': [
            'ai-agent=aiagent.main:main',
        ],
    },
)
