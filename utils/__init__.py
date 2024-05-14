def strtobool(value):
    """Convert a string representation of truth to True or False."""
    return value.lower() in {"true", "t", "yes", "y", "1"}
