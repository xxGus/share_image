import re


__email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def validate_email(email):
    """Verify if an email address is valid."""
    return __email_format_is_valid(email)

def __email_format_is_valid(email):
    """Verify if the email format is valid."""
    if not email:
        return False
    return __email.match(email)