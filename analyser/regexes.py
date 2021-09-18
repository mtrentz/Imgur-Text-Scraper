REGEX_DETECTION_LIST = {
    'email': [
        r'email',
        r'mail',
        r'[^@\s]+@[^@\s\.]+\.[^@\.\s]+',
    ],
    'password': [
        r'password',
    ],
    'crypto': [
        r'bitcoin',
        r'bit',
        r'crypto',
        r'binance',
        # Bitcoin wallet regex
        r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}',
        # Eth wallet regex
        r'0x[a-fA-F0-9]{30,40}'
    ],
    'phone': [
        # US phone
        r'\([0-9]{3}\)[0-9]{3}-[0-9]{4}',
        # Brazil phone
        r'\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*',
        # India phone
        r'\+?\d[\d -]{8,12}\d',
    ]
}