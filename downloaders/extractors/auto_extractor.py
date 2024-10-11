from typing import Dict, Union, List, Optional
from tqdm.auto import tqdm
from .base_extractor import BaseExtractor
from .gzip_extractor import GzipExtractor
from .targz_extractor import TargzExtractor
from .xz_extractor import XzExtractor
from .zip_extraction import ZipExtractor
from .bz2_extractor import BZ2Extractor
from .tar_extractor import TarExtractor


class AutoExtractor(BaseExtractor):
    """Class to automatically extract files."""

    def __init__(
        self, cache: bool = True, delete_original_after_extraction: bool = False
    ):
        """Create new file extractor.

        Parameters
        -------------------
        cache: bool = True,
            Whether to skip extraction when file is already available.
        delete_original_after_extraction: bool = False,
            Whether to delete the original file after it has been extracted.
        """
        super().__init__(
            None,
            cache=cache,
            delete_original_after_extraction=delete_original_after_extraction,
        )
        self._extractors = [
            extractor(
                cache=cache,
                delete_original_after_extraction=delete_original_after_extraction,
            )
            for extractor in (
                GzipExtractor,
                XzExtractor,
                BZ2Extractor,
                TargzExtractor,
                TarExtractor,
                ZipExtractor,
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
        """Return Whether this extractor can extract or not the given file.

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
        source: Union[str, List[str]],
        destination: Optional[Union[str, List[str]]] = None,
    ) -> List[Dict]:
        """Extract the given source file to the given destination.

        Parameters
        -------------------
        source: Union[str, List[str]],
            The source file to extract.
            If a list is provided, all files will be extracted.
        destination: Optional[Union[str, List[str]]] = None,
            The destination file to target.
            If it is not provided, the destination path
            will be inferred by the provided source paths.
            If a list is provided, we expect it to have the same length
            as the source list.

        Returns
        -------------------
        Dictionary with metadata.
        """
        if isinstance(source, str):
            source = [source]
        if destination is None:
            destination = [None] * len(source)
        elif isinstance(destination, str):
            destination = [destination]
        assert len(source) == len(destination), (
            "The source and destination lists must have the same length, "
            f"but got {len(source)} and {len(destination)} respectively."
        )

        return [
            self.get_supported_extractor(src).extract(src, dst)
            for src, dst in tqdm(
                zip(source, destination),
                desc="Extracting files",
                total=len(source),
                disable=len(source) == 1,
            )
        ]
