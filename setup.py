#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="jcm",
    version="1.0",
    description="Tool used to manage your jumpcloud account via the API",
    author="Joshua Goldman",
    author_email="joshgoldmanops@gmail.com",
    url="https://github.com/macgyverops/jcm",
    py_modules=['jcm'],
    install_requires=[
        "click",
        "requests",
	"configparser",
    ],
    entry_points="""
        [console_scripts]
        jcm=jcm:cli
    """,
)
