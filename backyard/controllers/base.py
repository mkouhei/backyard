# -*- coding: utf-8 -*-
"""backyard.controllers.base."""
import sys
import pkg_resources
from backyard import __project__, __version__, __author__, __repo__, READTHEDOCS


def get_ver(pkg_name):
    """package version.

    :rtype: str
    :return: package version

    :param str pkg_name: package name
    """
    return pkg_resources.get_distribution(pkg_name).version


def meta():
    """This project meta data.

    :rtype: dict
    :return: this project meta data
    """
    return dict(project=__project__,
                depver={'python': sys.version.split()[0],
                        'pyramid': get_ver('pyramid')},
                version=__version__,
                author=__author__,
                repo=__repo__,
                docs=READTHEDOCS)
