import re
import structlog
import pycountry

logger = structlog.get_logger(__name__)


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
        A country code or a country name (e.g., "MY", "SG", "Singapore").
        If the input is empty or invalid, returns `DEFAULT_COUNTRY`.

    Examples
    --------
    >>> normalize_country("sg")
    "SG"
    >>> normalize_country("")
    "MY"
    """
    DEFAULT_COUNTRY = "MY"
    ALIASES: dict = {
        "uk": "GB",
        "u.k.": "GB",
        "england": "GB",
        "scotland": "GB",
        "usa": "US",
        "u.s.": "US",
        "america": "US",
    }

    # Strip the string and merge internal spaces into one space.
    country = country.strip()
    country = re.sub(r"\s+", " ", country)

    country_lower = country.lower()
    if country_lower in ALIASES:
        country = ALIASES[country_lower]

    # Empty or invalid country code.
    if not country or country == "" or country.lower() in {"nan", "none"}:
        logger.warning(
            "normalize_country_invalid",
            input_country=country,
            default_country=DEFAULT_COUNTRY,
            reason="invalid_input",
            action="set to default country",
        )
        return DEFAULT_COUNTRY

    try:
        result = pycountry.countries.lookup(country)
        logger.debug(
            "normalize_country_success",
            input_country=country,
            result_country=result.alpha_2,
        )
        return result.alpha_2
    except LookupError:
        logger.warning(
            "normalize_country_lookup_failed",
            input_country=country,
            default_country=DEFAULT_COUNTRY,
            reason="lookup_error",
            action="set to default country",
        )
        return DEFAULT_COUNTRY
