import tarfile
import gzip
import shutil
from .base_extractor import BaseExtractor
from .utils import is_gzip, is_targz


class GzipExtractor(BaseExtractor):
    """Extractor for Gzip files."""

    def __init__(
        self,
        cache: bool = True,
        delete_original_after_extraction: bool = True
    ):
        """Create new GzipExtractor object.

        Parameters
        -------------------
        cache: bool = True,
            Wether to skip extraction when file is already available.
        delete_original_after_extraction: bool = True,
            Wether to delete the original file after it has been extracted.
        """
        super().__init__(
            extension=".gz",
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
        return is_gzip(source) and not is_targz(source)

    def _extract(self, source: str, destination: str):
        """Extract the given source to the given destination.

        Parameters
        ------------------
        source: str,
            The source file.
        destination: str,
            The target destination.
        """
        with gzip.open(source, 'rb') as f_in:
            with open(destination, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
