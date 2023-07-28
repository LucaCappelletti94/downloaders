import tarfile
from .base_extractor import BaseExtractor
from .utils import is_targz


class TargzExtractor(BaseExtractor):
    """Extractor for Targz files."""

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
            extension=[".tar.gz", ".tgz"],
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
        return is_targz(source)

    def _extract(self, source: str, destination: str):
        """Extract the given source to the given destination.

        Parameters
        ------------------
        source: str,
            The source file.
        destination: str,
            The target destination.
        """
        with tarfile.open(source, "r:gz") as tar:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, destination)
