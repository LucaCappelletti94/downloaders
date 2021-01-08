from typing import Dict
from .base_extractor import BaseExtractor
from .gzip_extractor import GzipExtractor
from .targz_extractor import TargzExtractor
from .xz_extractor import XzExtractor
from .zip_extraction import ZipExtractor


class AutoExtractor(BaseExtractor):
    """Class to automatically extract files."""

    def __init__(
        self,
        cache: bool = True,
        delete_original_after_extraction: bool = False
    ):
        """Create new file extractor.

        Parameters
        -------------------
        cache: bool = True,
            Wether to skip extraction when file is already available.
        delete_original_after_extraction: bool = False,
            Wether to delete the original file after it has been extracted.
        """
        super().__init__(
            None,
            cache=cache,
            delete_original_after_extraction=delete_original_after_extraction
        )
        self._extractors = [
            extractor(
                cache=cache,
                delete_original_after_extraction=delete_original_after_extraction
            )
            for extractor in (
                GzipExtractor,
                TargzExtractor,
                XzExtractor,
                ZipExtractor
            )
        ]

    def get_supported_extractor(self, source: str) -> BaseExtractor:
        """Return supported extractor if it exists.

        Parameters
        --------------------
        source: str,
            The source path to test if it can be extracted.

        Returns
        --------------------
        BaseExtractor if one exists, None otherwise.
        """
        for extractor in self._extractors:
            if extractor.can_extract(source):
                return extractor
        return None

    def destination_path(self, source: str) -> str:
        """Return destination path from given source.

        Parameters
        ----------------------
        source: str,
            The source path to be used to generate the expected destination path.

        Returns
        ----------------------
        The extracted path
        """
        return self.get_supported_extractor(source).destination_path(source)

    def can_extract(self, source: str) -> bool:
        """Return wether this extractor can extract or not the given file.

        Parameters
        --------------------
        source: str,
            The source path to test if it can be extracted.

        Returns
        --------------------
        Boolean value representing if the file can be extracted.
        """
        return self.get_supported_extractor(source) is not None

    def extract(
        self,
        source: str,
        destination: str = None
    ) -> Dict:
        """Extract the given source file to the given destination.

        Parameters
        -------------------
        source: str,
            The source file to extract.
        destination: str = None,
            The destination file to target.

        Returns
        -------------------
        Dictionary with metadata.
        """
        return self.get_supported_extractor(source).extract(
            source,
            destination
        )
