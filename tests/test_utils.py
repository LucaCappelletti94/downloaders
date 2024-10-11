"""Test the utils module.""" ""
from glob import glob

from downloaders.extractors.utils import is_gzip, is_targz, is_xz


def test_utils():
    """Test if gzip file is recognized correctly and all the others are not."""
    paths = glob("tests/data/*")
    for path in paths:
        assert path.endswith("gz") == is_gzip(path)
        assert path.endswith("xz") == is_xz(path)
        assert path.endswith("tar.gz") == is_targz(path)
        assert (path.endswith("gz") and not path.endswith(".tar.gz")) == (
            not is_targz(path) and is_gzip(path)
        )
