#!/usr/bin/env python2

from setuptools import setup
from gerbmerge.__version_info__ import __version__

setup(
    name = "gerbmerge",
    version = __version__,
    license = "GPLv3",
    description = "Merge multiple Gerber/Excellon files",
    long_description = \
"""GerbMerge is a program that combines several Gerber
(i.e., RS274-X) and Excellon files into a single set
of files. This program is useful for combining multiple
printed circuit board layout files into a single job.""",
    author = "Rugged Circuits LLC",
    author_email = "support@ruggedcircuits.com",
    maintainer = "stertingen",
    maintainer_email = "stertingen@yahoo.com",
    url = "https://github.com/stertingen/gerbmerge",
    packages = ["gerbmerge"],
    python_requires = ">=2.4,<3",
    use_2to3 = False,
    install_requires = ["simpleparse>=2.1.0"],
    entry_points = {
        'console_scripts': ['gerbmerge = gerbmerge.gerbmerge:main'],
        'setuptools.installation': ['eggsecutable = gerbmerge.gerbmerge:main']
    },
    include_package_data = True
)
