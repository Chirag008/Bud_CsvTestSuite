import csv
import re
from enum import Enum

import pandas as pd

from src import is_date
from src.Patterns import Patterns
pp = Patterns()


class ComparisonType(Enum):
    REGEX = 'regex'
    FUNCTION = 'function'


def get_csv_file_columns_list(csv_file_path, delimiter=','):
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        columns = None
        for row in csv_reader:
            columns = row
            break
        return columns


def get_csv_file_row_count(csv_file_path, should_count_header=True, delimiter=','):
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        return len(list(csv_reader)) if should_count_header else len(list(csv_reader)) - 1


def get_duplicate_records_count(csv_file_path, delimiter=','):
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    return df.duplicated().sum()


def get_column_name_to_type_mappping(csv_file_path, delimiter=','):
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    # check for boolean datatype. If column contains only 0 or 1 as values, then we take this as boolean data type
    mapping = dict()
    for col in df.columns:
        if 'int' in str(df[col].dtype) or 'float' in str(df[col].dtype):
            uniques = df[col].unique()
            if len(uniques) <= 2 and all(val in [0, 1] for val in list(uniques)):
                mapping[col] = 'boolean'
            else:
                mapping[col] = 'number'
        elif df[col].dtype == 'object':
            # check if it's a date column
            if is_date(df[col].iloc[df[col].first_valid_index()]):
                mapping[col] = 'date'
            else:
                mapping[col] = 'string'
    return mapping


def get_list_values_not_following_regex(csv_file_path, column_name, regex: str, delimiter=','):
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    regex = re.compile(regex)
    filtered_result = filter(lambda x: not is_value_matches_regex(x, regex), df[column_name].tolist())
    return list(filtered_result)


def get_list_values_not_following_condition(csv_file_path, column_name, comparison_func, delimiter=','):
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    filtered_result = filter(lambda x: not comparison_func(x), df[column_name].tolist())
    return list(filtered_result)


def is_value_matches_regex(value, regex):
    return bool(regex.match(str(value)))


if __name__ == '__main__':
    result = get_list_values_not_following_regex('../resources/csv/Customer_MR_NoDup.csv',
                                                 'MasterAccount',
                                                 '^[0|1]{1}$')
    print(result)
