"""Test module to test the base downloader with several compression algorithms."""
import os
import shutil
from downloaders import BaseDownloader


def test_base_downloader():
    """Test the base downloader with several compression algorithms."""
    root = "tests/downloads"
    urls = [
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/archive.tar?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/example.csv?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/example.csv.gz?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/example.csv.xz?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/example.tar.bz2?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/data.zip?raw=true",
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/test.tar.gz?raw=true",
    ]
    for cache in (True, False):
        for auto_extract in (True, False):
            if os.path.exists(root):
                shutil.rmtree(root)
            downloader = BaseDownloader(
                auto_extract=auto_extract,
                target_directory=root,
                verbose=True,
                cache=cache,
            )
            downloader.download(urls)
            downloader.download(urls)
            downloader.download(urls[0])
            downloader.download(urls[0], os.path.join(root, "archive.tar"))
            # if os.path.exists(root):
            #    shutil.rmtree(root)
