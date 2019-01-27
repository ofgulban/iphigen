"""Test utility functions."""

import pytest
import numpy as np
from iphigen.utils import truncate_range, set_range, parse_filepath


def test_truncate_range():
    """Test range truncation."""
    # Given
    data = np.random.random(100)
    data.ravel()[np.random.choice(data.size, 10, replace=False)] = 0
    data.ravel()[np.random.choice(data.size, 5, replace=False)] = np.nan
    p_min, p_max = 2.5, 97.5
    expected = np.nanpercentile(data, [p_min, p_max])
    # When
    output = truncate_range(data, pmin=p_min, pmax=p_max,
                            discard_zeros=False)
    # Then
    assert all(np.nanpercentile(output, [0, 100]) == expected)


def test_set_range():
    """Test range scaling."""
    # Given
    data = np.random.random(100) - 0.5
    data.ravel()[np.random.choice(data.size, 10, replace=False)] = 0.
    data.ravel()[np.random.choice(data.size, 5, replace=False)] = np.nan
    s = 255
    expected = [0., s]  # min and max
    # When
    output = set_range(data, zero_to=s, discard_zeros=False)
    # Then
    assert all([np.nanmin(output) == pytest.approx(expected[0]),
                np.nanmax(output) == pytest.approx(expected[1])])


def test_parse_filepath():
    """Test file path parsing."""
    # Given
    path = '/path/to/file.nii.gz'
    # When
    dirname, basename, ext = parse_filepath(path)
    # Then
    assert [dirname, basename, ext] == ['/path/to', 'file', 'nii.gz']
