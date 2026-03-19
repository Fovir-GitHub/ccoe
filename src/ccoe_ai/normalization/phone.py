import structlog
import phonenumbers

logger = structlog.get_logger(__name__)


def normalize_phone(number: str | None, country: str | None) -> str:
    """
    Normalize phone number according to country code.

    Parameters
    ----------
    number : str
        The input phone number, whichi may be empty or invalid.
    country : str
        The input country code.

    Returns
    -------
    str
        A normalized phone number in E.164 format.
        If the input is empty or invalid, returns `INVALID_NUMBER`.
    """
    INVALID_NUMBER = "N/A"

    if number is None or country is None:
        logger.error(
            "normalize_phone_missing_input",
            number=number,
            country=country,
        )
        return INVALID_NUMBER

    if number == "nan" or country == "nan":
        logger.error(
            "normalize_phone_failed",
            number=number,
            country=country,
            reason="nan_value",
        )
        return INVALID_NUMBER

    try:
        logger.debug(
            "normalize_phone_start",
            number=number,
            country=country,
        )
        parsed = phonenumbers.parse(number, country)
        if not phonenumbers.is_valid_number(parsed):
            logger.error(
                "normalize_phone_invalid_number",
                number=number,
                country=country,
                parsed_number=str(parsed),
            )
            return INVALID_NUMBER

        result = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        logger.debug(
            "normalize_phone_success",
            number=number,
            country=country,
            result=result,
        )
        return result
    except phonenumbers.NumberParseException as e:
        logger.error(
            "normalize_phone_parse_error",
            number=number,
            country=country,
            error=str(e),
        )
        return INVALID_NUMBER
