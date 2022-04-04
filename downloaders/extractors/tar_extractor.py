"""Submodule providing operator for extracting Tar files."""
import tarfile
from .base_extractor import BaseExtractor
from .utils import is_tar


class TarExtractor(BaseExtractor):
    """Extractor for Tar files."""

    def __init__(
        self,
        cache: bool = True,
        delete_original_after_extraction: bool = True
    ):
        """Create new TargzExtractor object.

        Parameters
        -------------------
        cache: bool = True,
            Wether to skip extraction when file is already available.
        delete_original_after_extraction: bool = True,
            Wether to delete the original file after it has been extracted.
        """
        super().__init__(
            extension=[".tar", ],
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
        return is_tar(source)

    def _extract(self, source: str, destination: str):
        """Extract the given source to the given destination.

        Parameters
        ------------------
        source: str,
            The source file.
        destination: str,
            The target destination.
        """
        with tarfile.open(source, "r") as tar:
            tar.extractall(destination)
