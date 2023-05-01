"""
A module for vectorized geohashing in Python.
Vectorized functions that allow efficient transformation of latitude and longitude coordinates into Map Tile
coordinates, Map Pixel coordinates or QuadKeys. This can be particularly useful in (GIS) geographic information systems
and mapping applications. By utilizing vectorized functions, transformation can be performed on large datasets,
with minimal impact on performance. Additionally, only using numpy as dependency these functions can be easily
incorporated into existing code and workflows.

Platform Support:
    This module is supported on Unix and Windows platforms.

Module Author:
    name : Filip Jakovljevic
    email : fillix96@gmail.com
"""
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

from .vec_geohash import *  # noqa: F403

try:
    __version__ = version("vec_geohash")
except PackageNotFoundError:
    # If the package is not installed, don't add __version__
    pass

__author__ = "FJakovljevic"
