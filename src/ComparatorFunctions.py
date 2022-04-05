class ComparatorFunctions:

    def __init__(self):
        pass

    def check_value_range_0_100(self, x):
        if type(x) == str:
            x = float(x) if '.' in x else int(x)
        return 0 <= x <= 100

    def check_is_value_a_number(self, x):
        if type(x) == int or type(x) == float:
            return True
        if type(x) == str:
            try:
                x = float(x)
                return True
            except ValueError as e:
                return False
