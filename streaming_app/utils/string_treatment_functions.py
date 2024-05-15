import unicodedata


def remove_accents(input_str):
    """
    Normalize strings to remove accents and perform a case-insensitive comparison.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])