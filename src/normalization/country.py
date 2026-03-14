import logging


def normalize_country(country: str) -> str:
    """
    Normalize country code.

    Parameters
    ----------
    country : str
        The input country code, which may be empty or invalid.

    Returns
    -------
    str
        A normalized two-letter country code (e.g., "MY", "SG").
        If the input is empty or invalid, returns `DEFAULT_COUNTRY`.

    Examples
    --------
    >>> normalize_country("sg")
    "SG"
    >>> normalize_country("")
    "MY"
    """

    import pycountry

    DEFAULT_COUNTRY = "MY"

    # Empty or invalid country code.
    if (
        not country
        or country.strip() == ""
        or country.strip().lower in {"nan", "none"}
        or len(country.strip()) != 2
        or pycountry.countries.get(alpha_2=country.upper()) is None
    ):
        logging.warning(
            "normalize country: invalid country code %s, set to default country %s",
            country,
            DEFAULT_COUNTRY,
        )
        return DEFAULT_COUNTRY

    try:
        result = pycountry.countries.lookup(country)
        return result.alpha_2
    except LookupError:
        logging.warning(
            "normalize country: invalid country code %s, set to default country %s",
            country,
            DEFAULT_COUNTRY,
        )
        return DEFAULT_COUNTRY
