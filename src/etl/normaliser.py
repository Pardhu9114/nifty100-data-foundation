import re

def normalize_year(value):
    if value is None:
        return None

    value = str(value).strip()

    if value.startswith("FY"):
        return 2000 + int(value[2:])

    match = re.search(r"\d{4}", value)

    if match:
        return int(match.group())

    raise ValueError(f"Invalid year: {value}")


def normalize_ticker(value):
    if value is None:
        return None

    return str(value).strip().upper()