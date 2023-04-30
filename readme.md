# Vec_GeoHash

![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://camo.githubusercontent.com/890acbdcb87868b382af9a4b1fac507b9659d9bf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d626c75652e737667)
![Tests](https://github.com/FJakovljevic/vec_geohash/actions/workflows/run_tests_with_conda.yml/badge.svg)

## Short Description

Vectorized functions that allow efficient transformation of __latitude and longitude coordinates__ into `Map Tile coordinates`, `Map Pixel coordinates` or `QuadKeys`. This can be particularly useful in (GIS) geographic information systems and mapping applications. By utilizing vectorized functions, transformation can be performed on large datasets, with minimal impact on performance. Additionally, only using numpy as dependency these functions can be easily incorporated into existing code and workflows.

## Instalation

```sh
pip install vec_geohash
```

## Usage

#### Vector example

```python
import vec_geohash

lat_vector = [53.1231276599, 41.85]
lon_vector = [82.6978699112, -87.65]
zoom = 9

# getting tiles as [tile_x] vector and [tile_y] vector
vec_geohash.lat_lon_to_tile(lat_vector, lon_vector, zoom)
>>> (array([373, 131]), array([166, 190]))

# getting tiles as [[tile_x, tile_y]] vector
vec_geohash.lat_lon_to_tile(lat_vector, lon_vector, zoom)
>>> array([[373, 166],
           [131, 190]])

# getting quadkey
vec_geohash.lat_lon_to_quadkey(lat_vector, lon_vector, zoom)
>>> array(['121310321', '030222231'], dtype='<U9')

# getting pixels as [pixel_x] vector and [pixel_y] vector
vec_geohash.lat_lon_to_pixel(lat_vector, lon_vector, zoom)
>>> (array([95645, 33623]), array([42622, 48729]))

# getting pixels as [[pixel_x, pixel_y]] vector
vec_geohash.lat_lon_to_pixel(lat_vector, lon_vector, zoom)
>>> array([[95645, 42622],
           [33623, 48729]])
```

#### Scalar example

```python
import vec_geohash

lat = 53.1231276599
lon = 82.6978699112
zoom = 9

# getting tiles 
vec_geohash.lat_lon_to_tile(lat, lon, zoom)
>>> (373, 166)

# getting quadkey
vec_geohash.lat_lon_to_quadkey(lat, lon, zoom)
>>> array(['121310321'], dtype='<U9')

# getting pixels
vec_geohash.lat_lon_to_pixel(lat, lon, zoom)
>>> (95645, 42622)
```