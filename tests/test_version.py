"""Tests for the package version."""
from validate_version_code import validate_version_code
from downloaders.__version__ import __version__


def test_version():
    """Test that the version code conforms to PEP-440."""
    assert validate_version_code(__version__)
