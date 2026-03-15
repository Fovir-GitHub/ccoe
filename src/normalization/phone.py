import logging


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

    import phonenumbers

    INVALID_NUMBER = "N/A"

    if number is None or country is None:
        logging.error("normalize phone number: empty number or country")
        return INVALID_NUMBER

    if number == "nan" or country == "nan":
        logging.error(
            "normalize phone number failed: number=%s country=%s", number, country
        )
        return INVALID_NUMBER

    try:
        logging.debug("normalize phone number number=%s country=%s", number, country)
        parsed = phonenumbers.parse(number, country)
        if not phonenumbers.is_valid_number(parsed):
            logging.error("invalid number number=%s", parsed)
            return INVALID_NUMBER

        result = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        logging.debug("normalize phone number number=%s result=%s", number, result)
        return result
    except phonenumbers.NumberParseException:
        logging.error("parse number failed number=%s country=%s", number, country)
        return INVALID_NUMBER
