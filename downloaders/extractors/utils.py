import lzma
import os
import tarfile


def is_gzip(source: str) -> bool:
    """Return wether the given file is a gzip.

    Parameters
    --------------------
    source: str,
        The source path to test if it can be extracted.

    Returns
    --------------------
    Boolean value representing if the is a gzip.
    """
    if not os.path.exists(source):
        return False
    if source.endswith(".gz"):
        return True
    with open(source, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'


def is_xz(source: str) -> bool:
    """Return wether the given file is a xz.

    Parameters
    --------------------
    source: str,
        The source path to test if it can be extracted.

    Returns
    --------------------
    Boolean value representing if the is a xz.
    """
    if not os.path.exists(source):
        return False
    if source.endswith(".xz"):
        return True
    with lzma.open(source, 'r') as f:
        try:
            f.read(1)
            return True
        except lzma.LZMAError:
            return False


def is_targz(source: str) -> bool:
    """Return wether the given file is a targz.

    Parameters
    --------------------
    source: str,
        The source path to test if it can be extracted.

    Returns
    --------------------
    Boolean value representing if the file is a targz.
    """
    if not os.path.exists(source):
        return False
    if source.endswith(".tar.gz"):
        return True
    return tarfile.is_tarfile(source) and is_gzip(source)
