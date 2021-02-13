from typing import List, Union
import os


class BaseExtractor:
    """Base class for extracting a compress file."""

    def __init__(
        self,
        extension: Union[str, List[str]],
        cache: bool = True,
        delete_original_after_extraction: bool = True
    ):
        """Create new BaseExtractor object.

        Parameters
        -------------------
        extension: Union[str, List[str]],
            The base extractor extension.
        cache: bool = True,
            Wether to skip extraction when file is already available.
        delete_original_after_extraction: bool = True,
            Wether to delete the original file after it has been extracted.
        """
        if isinstance(extension, str):
            extension = [extension]
        self._extensions = extension
        self._cache = cache
        self._delete_original_after_extraction = delete_original_after_extraction

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
        raise NotImplementedError(
            "The method can_extract must be implemented in child classes."
        )

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
        # If the file ends with the expected extension we return the updated
        # path.
        for ext in self._extensions:
            if source.endswith(ext):
                return source[:-len(ext)]
        # Otherwise, we have no clue what path may be optimal, hence we just
        # add the additional extension "extracted".
        return "{}.extracted".format(source)

    def _extract(self, source: str, destination: str):
        """Extract the given source to the given destination.

        Parameters
        ------------------
        source: str,
            The source file.
        destination: str,
            The target destination.
        """
        raise NotImplementedError(
            "The method _extract must be implemented in child classes."
        )

    def is_cached(self, destination: str) -> bool:
        """Return boolean representing if given path is cached."""
        return self._cache and os.path.exists(destination)

    def extract(
        self,
        source: str,
        destination: str = None
    ):
        """Extract the given source file to the given destination.

        Parameters
        -------------------
        source: str,
            The source file to extract.
        destination: str = None,
            The destination file to target.
        """
        cached = False
        success = False
        # If the destinations is not given, we obtain it from the source.
        if destination is None:
            destination = self.destination_path(source)
        # If the cache is enabled and the file is cached.
        if not self.is_cached(destination):
            # Create the folders if necessary.
            directory = os.path.dirname(destination)
            # If the directory is not the current one.
            if directory:
                os.makedirs(
                    directory,
                    exist_ok=True
                )
            # Try to extract the file, if it fails we delete it.
            try:
                self._extract(source, destination)
                if self._delete_original_after_extraction:
                    os.remove(source)
            except (Exception, KeyboardInterrupt) as e:
                # If the extracted file has been created
                if os.path.exists(destination):
                    os.remove(destination)
                raise e
            success = True
        else:
            cached = True
            success = True

        return {
            "file_size": os.path.getsize(destination),
            "destination": destination,
            "cached": cached,
            "success": success,
        }
