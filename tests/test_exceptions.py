"""Test moduke to test exceptions and corner cases."""
import pytest
from downloaders import BaseDownloader


def test_exceptions():
    """Testing corner cases that raise exceptions."""
    with pytest.raises(ValueError):
        BaseDownloader(process_number=0)
    with pytest.raises(ValueError):
        BaseDownloader(process_number=[])
    downloader = BaseDownloader(crash_early=True)
    with pytest.raises(ValueError):
        downloader.download(urls=["lo_url"], paths=[7, 7, 5])
    with pytest.raises(ValueError):
        downloader.download(
            "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/not_existing.tar?raw=true",
        )
