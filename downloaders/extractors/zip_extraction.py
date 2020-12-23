import zipfile
from .base_extractor import BaseExtractor


class ZipExtractor(BaseExtractor):
    """Extractor for Gzip files."""

    def __init__(
        self,
        cache: bool = True,
        delete_original_after_extraction: bool = True
    ):
        """Create new ZipExtractor object.

        Parameters
        -------------------
        cache: bool = True,
            Wether to skip extraction when file is already available.
        delete_original_after_extraction: bool = True,
            Wether to delete the original file after it has been extracted.
        """
        super().__init__(
            extension=".zip",
            cache=cache,
            delete_original_after_extraction=delete_original_after_extraction
        )

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
        return zipfile.is_zipfile(source)

    def _extract(self, source: str, destination: str):
        """Extract the given source to the given destination.

        Parameters
        ------------------
        source: str,
            The source file.
        destination: str,
            The target destination.
        """
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(destination)
