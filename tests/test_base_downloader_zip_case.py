"""Test module to test the base downloader with a zip file case."""
from downloaders import BaseDownloader


def test_base_downloader_zip_case():
    """Test the base downloader with a zip file case."""
    root = "tests/downloads"
    urls = [
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/data.zip?raw=true",
    ]
    downloader = BaseDownloader(
        target_directory=root,
    )
    downloader.download(urls)
