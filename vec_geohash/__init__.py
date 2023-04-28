"""
A module for vectorized geohashing in Python.

This module provides functions for converting geographic coordinates (latitude
and longitude) to a geohash string, and vice versa. The functions are vectorized
to support processing of large arrays of coordinates in a fast and efficient
manner.


Functions
---------


Platform Support
----------------
This module is supported on Unix and Windows platforms.


Module Author
-------------
    name : Filip Jakovljevic
    email : fillix96@gmail.com
"""

from .vec_geohash import *

__author__ = 'FJakovljevic'

try:
    import numpy
except ImportError:
    import logging
    logging.error(f"Numpy is a needed dependency to use vectorised geohashing functions.")