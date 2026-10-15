import re

def extract_order_id(text: str):
    """
    Extracts an order ID like ORD12345 from user input.
    """

    match = re.search(r'ORD\d+', text.upper())

    if match:
        return match.group()

    return None