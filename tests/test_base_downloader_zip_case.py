import os
from downloaders import BaseDownloader
import shutil


def test_base_downloader_zip_case():
    root = "tests/downloads"
    urls = [
        "https://github.com/LucaCappelletti94/downloaders/blob/main/tests/data/data.zip?raw=true",
    ]
    downloader = BaseDownloader(
        target_directory=root,
    )
    downloader.download(urls)