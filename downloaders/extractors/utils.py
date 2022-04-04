import lzma
import os
import tarfile


def is_bzip2(source: str) -> bool:
    """Return wether the given file is a bzip2.

    Parameters
    --------------------
    source: str,
        The source path to test if it can be extracted.

    Returns
    --------------------
    Boolean value representing if the is a bzip2.
    """
    if source.endswith(".bz2"):
        return True
    return False


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
    if source.endswith(".gz"):
        return True
    if not os.path.exists(source):
        return False
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
    if source.endswith(".xz"):
        return True
    if not os.path.exists(source):
        return False
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
    if source.endswith(".tar.gz"):
        return True
    if not os.path.exists(source):
        return False
    return tarfile.is_tarfile(source) and is_gzip(source)


def is_tar(source: str) -> bool:
    """Return wether the given file is a tar and NOT a targz.

    Parameters
    --------------------
    source: str,
        The source path to test if it can be extracted.

    Returns
    --------------------
    Boolean value representing if the file is a tar.
    """
    if source.endswith(".tar"):
        return True
    if not os.path.exists(source):
        return False
    return tarfile.is_tarfile(source) and not is_gzip(source)
