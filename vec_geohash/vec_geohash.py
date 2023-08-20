import numpy as np

TILE_SIZE = 256
BASE_4 = np.array(["0", "1", "2", "3"], dtype="<U1")


def _project_longitude(longitude):
    """
    Projects a vector of longitudes to the interval [0, 1].
    """
    return 0.5 + np.clip(longitude, -180, 180) / 360


def _project_latitude(latitude):
    """
    Projects a vector of latitudes to the interval [0, 0.99999].
    This limits the latitude to the range [-85.05112877, 85.05112877] degrees.
    """
    sin_y = np.sin((np.clip(latitude, -85.05112877, 85.05112877) * np.pi) / 180)
    return 0.5 - np.log((1 + sin_y) / (1 - sin_y)) / (4 * np.pi)


def project(latitude, longitude):
    """
    Projects vectors of latitude and longitude to the interval [0, 0.99999] and [0, 1], respectively.
    """
    return _project_longitude(longitude), _project_latitude(latitude)


################################################ to TILE
##############################################
def _projection_to_tile(x, zoom):
    """
    Returns the tile coordinate based on zoom level for a given projected latitude or longitude.
    """
    return np.int_(x * (1 << zoom))


def lat_lon_to_tile(latitude, longitude, zoom):
    """
    Returns the [tile_x] and [tile_y] coordinates for given vectors of latitude, longitude and zoom level.
    """
    proj_x, proj_y = _project_longitude(longitude), _project_latitude(latitude)
    return _projection_to_tile(proj_x, zoom), _projection_to_tile(proj_y, zoom)


def lat_lon_to_tile_tuple(latitude, longitude, zoom):
    """
    Returns the [[tile_x, tile_y]] coordinates for given vectors of latitude, longitude and zoom level.
    """
    tile_x, tile_y = lat_lon_to_tile(latitude, longitude, zoom)
    return np.array((tile_x, tile_y)).T


def pixel_to_tile(pixel_x, pixel_y):
    """
    Returns the [tile_x] and [tile_y] coordinates for given vectors of pixel_x and pixel_y coordinates.
    """
    return np.int_(pixel_x // TILE_SIZE), np.int_(pixel_y // TILE_SIZE)


def pixel_to_tile_tuple(pixel_x, pixel_y):
    """
    Returns the [[tile_x, tile_y]] coordinates for given vectors of pixel_x and pixel_y coordinates.
    """
    tile_x, tile_y = pixel_to_tile(pixel_x, pixel_y)
    return np.array((tile_x, tile_y)).T


def pixel_tuple_to_tile_tuple(pixel_tuple):
    """
    Returns the [[tile_x, tile_y]] coordinates for given vector of [[pixel_x], [pixel_y]] coordinates.
    """
    return np.int_(pixel_tuple // TILE_SIZE)


def quadkey_to_tile(quadkeys):
    """
    Converts QuadKeys to vectors of [tile_x] and [tile_y] coordinates.
    """
    if isinstance(quadkeys, list):
        quadkeys = np.array(quadkeys, dtype="U").reshape(len(quadkeys), 1)
    elif isinstance(quadkeys, str):
        quadkeys = np.array(quadkeys, dtype="U").reshape(1, 1)

    quadkeys = quadkeys.view("U1").astype(np.int_)
    shift_sequence = np.arange(quadkeys.shape[-1])[::-1]

    to_tile_y = ((quadkeys & 0b10) >> 1) << shift_sequence
    to_tile_x = (quadkeys & 0b01) << shift_sequence
    return to_tile_x.sum(1), to_tile_y.sum(1)


def quadkey_to_tile_tuple(quadkeys):
    """
    Converts QuadKeys to vector of tile tuple [[tile_x, tile_y]] coordinates.
    """
    tile_x, tile_y = quadkey_to_tile(quadkeys)
    return np.array((tile_x, tile_y)).T


##############################################
################################################


################################################ to QuadKey
##############################################
def _broadcast_array(x, repeat):
    """
    Broadcasts array X to a shape of (repeat, len(X))

                                     [[1, 1, 1, 1, 1]
    _broadcast_array([1,5,7], 5) -->  [5, 5, 5, 5, 5]
                                      [7, 7, 7, 7, 7]]
    """
    return np.broadcast_to(x, (repeat, x.size)).T


def _interleave_base4(tile_x_broadcasted, tile_y_broadcasted, zoom):
    """
    To convert tile coordinates into a quadkey, the bits of the Y and X coordinates are interleaved,
    and the result is interpreted as a base-4 number (with leading zeros maintained) and converted into a string.
    For instance, given tile XY coordinates of (3, 5) at level 3, the quadkey is determined as follows:
        tileX = 3 = 0112
        tileY = 5 = 1012
        quadkey = 1001112= 2134= “213”
    """
    shift_sequence = np.arange(zoom)[::-1]
    part_y = (np.right_shift(tile_y_broadcasted, shift_sequence) & 0b1) << 1
    part_x = np.right_shift(tile_x_broadcasted, shift_sequence) & 0b1
    return BASE_4[part_y | part_x].view(f"U{zoom}")


def tile_to_quadkey(tile_x, tile_y, zoom):
    """
    Converts [tile_x] and [tile_y] vectors to [quadkey] for zoom level `zoom`.
    The `zoom` level used here should be the same as the one used to create the tiles.
    """
    tile_x_broadcasted = _broadcast_array(np.int_(tile_x), zoom)
    tile_y_broadcasted = _broadcast_array(np.int_(tile_y), zoom)
    return _interleave_base4(tile_x_broadcasted, tile_y_broadcasted, zoom).flatten()


def lat_lon_to_quadkey(latitude, longitude, zoom):
    """Converts [latitude] and [longitude] vectors to [quadkey] for wanted zoom level."""
    tile_x, tile_y = lat_lon_to_tile(latitude, longitude, zoom)
    return tile_to_quadkey(tile_x, tile_y, zoom)


def pixel_to_quadkey(pixel_x, pixel_y, zoom):
    """Converts [pixel_x] and [pixel_y] vectors to [quadkey]."""
    tile_x, tile_y = pixel_to_tile(pixel_x, pixel_y)
    return tile_to_quadkey(tile_x, tile_y, zoom)


##############################################
################################################


################################################ to PIXEL
##############################################
def _projection_to_pixel(x, zoom):
    """Returns a PIXEL coordinate based on zoom level for projected lat/lon."""
    return np.int_(x * (TILE_SIZE << zoom))


def lat_lon_to_pixel(latitude, longitude, zoom):
    """Returns [pixel_x] and [pixel_y] coords for zoom level."""
    proj_x, proj_y = _project_longitude(longitude), _project_latitude(latitude)
    return _projection_to_pixel(proj_x, zoom), _projection_to_pixel(proj_y, zoom)


def lat_lon_to_pixel_tuple(latitude, longitude, zoom):
    """Returns [(pixel_x, pixel_y)] coords for zoom level."""
    pixel_x, pixel_y = lat_lon_to_pixel(latitude, longitude, zoom)
    return np.array((pixel_x, pixel_y)).T


def tile_to_pixel(tile_x, tile_y):
    """Convert [tile_x] and [tile_y] vectors to [[min_x, min_y, max_x, max_y]] pixel coordinates."""
    return np.array(
        (
            tile_x * TILE_SIZE,
            tile_y * TILE_SIZE,
            (tile_x + 1) * TILE_SIZE,
            (tile_y + 1) * TILE_SIZE,
        )
    ).T


def quadkey_to_pixel(quadkeys):
    """Convert [quadkey] vector to [[min_x, min_y, max_x, max_y]]  pixel coordinates."""
    tile_x, tile_y = quadkey_to_tile(quadkeys)
    return tile_to_pixel(tile_x, tile_y)


##############################################
################################################


################################################ to LatLon
##############################################
def _pixel_to_projection(x, zoom):
    """Transforms pixel coordinate to range [0, 1]."""
    max_pixel = TILE_SIZE << zoom
    return np.clip(x, 0, max_pixel) / max_pixel


def _tile_to_projection(x, zoom):
    """Transforms tile to projection."""
    return x / (1 << zoom)


def _projection_to_latitude(y):
    """Returns latitude from projection value."""
    return 90 - 360 * np.arctan(np.exp((y - 0.5) * 2 * np.pi)) / np.pi


def _projection_to_longitude(x):
    """Returns longitude from projection value."""
    return 360 * (x - 0.5)


def _tile_to_latitude(x, zoom):
    """Gets latitude of top left corner of tile."""
    return _projection_to_latitude(_tile_to_projection(x, zoom))


def _tile_to_longitude(x, zoom):
    """Gets latitude of top left corner of tile."""
    return _projection_to_longitude(_tile_to_projection(x, zoom))


def tile_to_lat_lon(tile_x, tile_y, zoom):
    """Convert [tile_x] and [tile_y] vectors to [[min_lon, min_lat, max_lon, max_lat]]."""
    min_lon = _tile_to_longitude(tile_x, zoom)
    max_lat = _tile_to_latitude(tile_y, zoom)
    max_lon = _tile_to_longitude(tile_x + 1, zoom)
    min_lat = _tile_to_latitude(tile_y + 1, zoom)
    return np.array((min_lon, min_lat, max_lon, max_lat)).T.reshape(-1, 4)


def quadkey_to_lat_lon(quadkeys):
    """Convert [quadkey] vector to [[min_lon, min_lat, max_lon, max_lat]]."""
    zoom = len(quadkeys) if isinstance(quadkeys, str) else len(quadkeys[0])
    tile_x, tile_y = quadkey_to_tile(quadkeys)
    return tile_to_lat_lon(tile_x, tile_y, zoom)


def pixel_to_lat_lon(pixel_x, pixel_y, zoom):
    """Converts [pixel_x] and [pixel_y] vectors to [latitude] and [longitude] for zoom level."""
    proj_x, proj_y = _pixel_to_projection(pixel_x, zoom), _pixel_to_projection(pixel_y, zoom)
    return _projection_to_latitude(proj_y), _projection_to_longitude(proj_x)


def pixel_to_lat_lon_tuple(pixel_x, pixel_y, zoom):
    """Converts [pixel_x] and [pixel_y] vectors to [[latitude, longitude]] for zoom level."""
    lat, lon = pixel_to_lat_lon(pixel_x, pixel_y, zoom)
    return np.array((lat, lon)).T


def pixel_tuple_to_lat_lon_tuple(latitude, longitude, zoom):
    "TODO"


##############################################
################################################


################################################ boundaries
##############################################
def lat_lon_bounds_to_tile_range(bounds, zoom):
    """Converts bounds [[min_lon, min_lat, max_lon, max_lat]] from GeoDataFrame to tile coords [[min_x, min_y, max_x, max_y]]."""
    lon_min, lat_min, lon_max, lat_max = bounds.T
    tile_x_min, tile_y_min = lat_lon_to_tile(lat_max, lon_min, zoom)
    tile_x_max, tile_y_max = lat_lon_to_tile(lat_min, lon_max, zoom)
    return np.array([tile_x_min, tile_y_min, tile_x_max, tile_y_max]).T
