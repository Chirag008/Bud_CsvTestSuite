class Patterns:
    boolean = r'^[0|1]{1}$'
    date = r'^[0|1]?\d{1}[/-][0|1|2|3]?\d{1}[/-][1|2]{1}[\d]{3}$'
    email = r'^[a-zA-Z0-9+_.-]+@[a-zA-Z]+[.]com$'
    number_or_decimal = r'^[\d]*[.]?[\d]+$'
    phone_number = r'^\d{3}-\d{3}-\d{4}$'

    def __init__(self):
        pass
