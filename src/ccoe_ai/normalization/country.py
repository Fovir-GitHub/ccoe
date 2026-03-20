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
        A normalized two-letter country code (e.g., "MY", "SG").
        If the input is empty or invalid, returns `DEFAULT_COUNTRY`.

    Examples
    --------
    >>> normalize_country("sg")
    "SG"
    >>> normalize_country("")
    "MY"
    """
    DEFAULT_COUNTRY = "MY"

    # Empty or invalid country code.
    if (
        not country
        or country.strip() == ""
        or country.strip().lower() in {"nan", "none"}
        or len(country.strip()) != 2
        or pycountry.countries.get(alpha_2=country.upper()) is None
    ):
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
