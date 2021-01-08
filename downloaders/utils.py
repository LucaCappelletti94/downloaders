def is_iterable(candidate) -> bool:
    """Return boolean value representing if object is iterable."""
    try:
        iter(candidate)
        return True
    except TypeError:
        return False
