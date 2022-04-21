"""
------------------------------------------------------------------------------
Kmaintainer <https://github.com/fjmaro/Kmaintainer>
Copyright 2022 Francisco José Mata Aroco

This file is part of Kmaintainer (hereinafter called "Library").

This "Library" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the licence, or
(at your option) any later version.

This "Library" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See LICENSE.md for more details.
------------------------------------------------------------------------------
"""

# pylint: disable=line-too-long
from distutils.core import setup
import kmaintainer


with open("README.md", "r", encoding='utf-8') as fhd:
    long_description = fhd.read()

setup(name="Kmaintainer",
      version=kmaintainer.__version__,
      license="GPLv3+",
      author=kmaintainer.__author__,
      url="https://github.com/fjmaro/Kmaintainer",
      description="Python script for photography and media files-original-date maintenance",
      long_description=long_description,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Programming Language :: Python :: 3",
          "Topic :: Multimedia"],
      packages=["kmaintainer", ],
      python_requires='>=3.9',
      install_requires=['kjmarotools @ git+https://github.com/fjmaro/KjmaroTools@main', ]
      )
