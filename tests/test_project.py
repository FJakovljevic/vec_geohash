import unittest

import numpy as np
import vec_geohash


class TestLatLon(unittest.TestCase):
    def test_latlon_single(self):
        # test input values
        lat = 53.1231276599
        lon = 82.6978699112
        zoom = 9

        # expected output for tile tuple
        expected_output = (373, 166)
        self.assertEqual(vec_geohash.lat_lon_to_tile(lat, lon, zoom), expected_output)

        # expected output for quadkey
        expected_output = np.array(["121310321"], dtype="<U9")
        np.testing.assert_array_equal(
            vec_geohash.lat_lon_to_quadkey(lat, lon, zoom), expected_output
        )

        # expected output for pixel tuple
        expected_output = (95645, 42622)
        np.testing.assert_array_equal(
            vec_geohash.lat_lon_to_pixel(lat, lon, zoom), expected_output
        )

    def test_latlon_vector(self):
        # test input values
        lat = np.array([53.1231276599, 41.85])
        lon = np.array([82.6978699112, -87.65])
        zoom = 9

        # expected output for tile tuple
        expected_output = np.array([[373, 166], [131, 190]])
        np.testing.assert_array_equal(
            vec_geohash.lat_lon_to_tile_tuple(lat, lon, zoom), expected_output
        )

        # expected output for quadkey
        expected_output = np.array(["121310321", "030222231"], dtype="<U9")
        np.testing.assert_array_equal(
            vec_geohash.lat_lon_to_quadkey(lat, lon, zoom), expected_output
        )

        # expected output for pixel tuple
        expected_output = np.array([[95645, 42622], [33623, 48729]])
        np.testing.assert_array_equal(
            vec_geohash.lat_lon_to_pixel_tuple(lat, lon, zoom), expected_output
        )


class TestPixel(unittest.TestCase):
    def test_pixel_single(self):
        # test input values
        lat = 95645
        lon = 42622
        zoom = 9

        # expected output for tile tuple
        expected_output = (373, 166)
        self.assertEqual(vec_geohash.pixel_to_tile(lat, lon), expected_output)

        # expected output for quadkey
        expected_output = np.array(["121310321"], dtype="<U9")
        np.testing.assert_array_equal(
            vec_geohash.pixel_to_quadkey(lat, lon, zoom), expected_output
        )

        # expected output for latlon tuple
        expected_output = (53.1231276599, 82.6978699112)
        np.testing.assert_almost_equal(
            vec_geohash.pixel_to_lat_lon(lat, lon, zoom), expected_output, decimal=3
        )

    def test_pixel_vector(self):
        # test input values
        lat = np.array([95645, 33623])
        lon = np.array([42622, 48729])
        zoom = 9

        # expected output for tile tuple
        expected_output = np.array([[373, 166], [131, 190]])
        np.testing.assert_array_equal(
            vec_geohash.pixel_to_tile_tuple(lat, lon), expected_output
        )

        # expected output for quadkey
        expected_output = np.array(["121310321", "030222231"], dtype="<U9")
        np.testing.assert_array_equal(
            vec_geohash.pixel_to_quadkey(lat, lon, zoom), expected_output
        )

        # expected output for latlon tuple
        expected_output = np.array([[53.1231276599, 82.6978699112], [41.851, -87.652]])
        np.testing.assert_almost_equal(
            vec_geohash.pixel_to_lat_lon_tuple(lat, lon, zoom),
            expected_output,
            decimal=3,
        )


class TestTile(unittest.TestCase):
    def test_tile_single(self):
        # test input values
        tile_x = 1
        tile_y = 1
        zoom = 1

        # expected output for quadkey
        expected_output = np.array(["3"], dtype="<U1")
        np.testing.assert_array_equal(
            vec_geohash.tile_to_quadkey(tile_x, tile_y, zoom), expected_output
        )

        # expected output for latlon
        expected_output = np.array([[0.0, -85.05112878, 180.0, 0.0]])
        np.testing.assert_almost_equal(
            vec_geohash.tile_to_lat_lon(tile_x, tile_y, zoom), expected_output
        )

        # expected output for pixel
        expected_output = np.array([256, 256, 512, 512])
        np.testing.assert_array_equal(
            vec_geohash.tile_to_pixel(tile_x, tile_y), expected_output
        )

    def test_tile_vec(self):
        # test input values
        tile_x = np.array([0, 3])
        tile_y = np.array([0, 3])
        zoom = 2

        # expected output for quadkey
        expected_output = np.array(["00", "33"], dtype="<U2")
        np.testing.assert_array_equal(
            vec_geohash.tile_to_quadkey(tile_x, tile_y, zoom), expected_output
        )

        # expected output for latlon
        expected_output = np.array(
            [
                [-180.0, 66.5132604, -90.0, 85.0511288],
                [90.0, -85.0511288, 180.0, -66.5132604],
            ]
        )
        np.testing.assert_almost_equal(
            vec_geohash.tile_to_lat_lon(tile_x, tile_y, zoom), expected_output
        )

        # expected output for pixel
        expected_output = np.array([[0, 0, 256, 256], [768, 768, 1024, 1024]])
        np.testing.assert_array_equal(
            vec_geohash.tile_to_pixel(tile_x, tile_y), expected_output
        )


class TestQuadkey(unittest.TestCase):
    def test_quadkey_single(self):
        quadkey = "121310321"

        # expected output for tile tuple
        expected_output = np.array([[373, 166]])
        np.testing.assert_array_equal(
            vec_geohash.quadkey_to_tile_tuple(quadkey), expected_output
        )

        # expected output for latlon
        expected_output = np.array([[82.265625, 52.908902, 82.96875, 53.330873]])
        np.testing.assert_almost_equal(
            vec_geohash.quadkey_to_lat_lon(quadkey), expected_output
        )

        # expected output for pixel
        expected_output = np.array([[95488, 42496, 95744, 42752]])
        np.testing.assert_almost_equal(
            vec_geohash.quadkey_to_pixel(quadkey), expected_output
        )

    def test_quadkey_vector(self):
        quadkey = ["121310321", "030222231"]

        # expected output for tile tuple
        expected_output = np.array([[373, 166], [131, 190]])
        np.testing.assert_array_equal(
            vec_geohash.quadkey_to_tile_tuple(quadkey), expected_output
        )

        # expected output for latlon
        expected_output = np.array(
            [
                [82.2656, 52.9089, 82.9687, 53.3308],
                [-87.8906, 41.5085, -87.1875, 42.0329],
            ]
        )
        np.testing.assert_almost_equal(
            vec_geohash.quadkey_to_lat_lon(quadkey), expected_output, decimal=3
        )

        # expected output for pixel
        expected_output = np.array(
            [[95488, 42496, 95744, 42752], [33536, 48640, 33792, 48896]]
        )
        np.testing.assert_almost_equal(
            vec_geohash.quadkey_to_pixel(quadkey), expected_output, decimal=3
        )


class TestProjection(unittest.TestCase):
    def test_project(self):
        # Test with basic inputs
        longitudes = np.array([0, 45, 90, 135, 180, -45, -90, -135, -180])
        expected_longitudes = np.array(
            [0.5, 0.625, 0.75, 0.875, 1, 0.375, 0.25, 0.125, 0]
        )

        latitudes = np.array([0, 30, 60, -30, -60])
        expected_latitudes = np.array([0.5, 0.4125752, 0.2903996, 0.5874248, 0.7096004])

        projected_longitudes, projected_latitudes = vec_geohash.project(
            latitudes, longitudes
        )
        np.testing.assert_almost_equal(projected_longitudes, expected_longitudes)
        np.testing.assert_almost_equal(projected_latitudes, expected_latitudes)

        # Test with single input value
        latitudes = 0
        longitudes = 0
        expected_longitudes = 0.5
        expected_latitudes = 0.5
        projected_longitudes, projected_latitudes = vec_geohash.project(
            latitudes, longitudes
        )
        np.testing.assert_approx_equal(projected_longitudes, expected_longitudes)
        np.testing.assert_approx_equal(projected_latitudes, expected_latitudes)

        # Test with input values exceeding limits
        latitudes = np.array([100, -100])
        expected_latitudes = np.array([0, 1])

        longitudes = np.array([190, -190])
        expected_longitudes = np.array([1, 0])

        projected_longitudes, projected_latitudes = vec_geohash.project(
            latitudes, longitudes
        )
        np.testing.assert_almost_equal(projected_longitudes, expected_longitudes)
        np.testing.assert_almost_equal(projected_latitudes, expected_latitudes)
