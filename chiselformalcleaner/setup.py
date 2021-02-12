#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  29/01/2020
#-----------------------------------------------------------------------------
#  Copyright (2020)  Armadeus Systems
#-----------------------------------------------------------------------------
""" setup
"""

from setuptools import setup, find_packages

setup(name="chiselformalcleaner",
      version="0.1",
      packages=find_packages(),
      scripts=['bin/chiselformalcleaner'],
      )
