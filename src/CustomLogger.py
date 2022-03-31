import logging
from enum import Enum


class ResultType(Enum):
    EXPECTED = 'Expected'
    ACTUAL = 'Actual'


class TxtColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


class CustomLogger:
    logger = None
    logs_separator = '-'

    def __init__(self, logger):
        self.logger = logger

    def print(self, log_message, result_type: ResultType = None, log_level='info',
              should_separate_by_dotted_lines=True):
        color = None
        if should_separate_by_dotted_lines:
            if result_type:
                if result_type == ResultType.EXPECTED:
                    color = TxtColors.OKBLUE
                else:
                    color = TxtColors.OKBLUE
                print(f"{TxtColors.BOLD}{color}"
                      f"{self.logs_separator * 45}  {result_type.value}  {self.logs_separator * 45}"
                      f"{TxtColors.ENDC}")
            else:
                print(self.logs_separator * 100)
            print(log_message)
            if color:
                print(f"{color}{self.logs_separator * 100}{TxtColors.ENDC}")
            else:
                print(self.logs_separator * 100)
        else:
            self.logger.log(logging.INFO, log_message)
