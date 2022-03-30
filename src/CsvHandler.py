import csv
import pandas as pd

from src import is_date


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


if __name__ == '__main__':
    mapping = get_column_name_to_type_mappping('../resources/csv/Customer_MR_NoDup.csv')
    print(mapping)
