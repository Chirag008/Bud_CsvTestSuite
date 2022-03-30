import pytest
import re
import logging
import src.CsvHandler as CsvHandler
import src.ExcelHandler as ExcelHandler

logger = logging.getLogger(__name__)


@pytest.fixture
def get_context():
    return {}


@pytest.mark.parametrize('input_csv_file_name',
                         ['Customer_MR_NoDup.csv'])
def test_TC_1_Validate_Excel_File_Naming_Convention(input_csv_file_name):
    csv_file_name_pattern = '.*.csv'
    logger.info('expected csv file pattern - {}'.format(csv_file_name_pattern))
    logger.info('Input csv file name - {}'.format(input_csv_file_name))
    file_name_matcher_regex = re.compile(csv_file_name_pattern)
    is_csv_name_as_per_standard = bool(file_name_matcher_regex.match(input_csv_file_name))
    logger.info('is csv name as per standard - {}'.format(is_csv_name_as_per_standard))
    assert is_csv_name_as_per_standard, 'input csv name not as per standards!'


@pytest.mark.parametrize('input_csv_file_path, schema_file_path',
                         [('resources/csv/Customer_MR_NoDup.csv',
                           'resources/mappings/Customer File to Cunexus Mapping - Grouped.xlsx')])
def test_TC_2_Validate_the_input_csv_file_schema(input_csv_file_path, schema_file_path):
    expected_col_name_to_type_mapping = ExcelHandler.get_column_name_to_column_type_mapping(schema_file_path)
    logger.info('Expected column name to column type - {}'.format(expected_col_name_to_type_mapping))
    actual_col_name_to_type_mapping = CsvHandler.get_column_name_to_type_mappping(input_csv_file_path)
    logger.info('Actual column name to column type - {}'.format(actual_col_name_to_type_mapping))
    list_mismatched_type_cols = []
    list_columns_not_found = []
    for col, col_type in expected_col_name_to_type_mapping.items():
        if col not in actual_col_name_to_type_mapping.keys():
            list_columns_not_found.append(col)
        else:
            if actual_col_name_to_type_mapping[col] != col_type:
                list_mismatched_type_cols.append(col)
    logger.info('mismatched data type columns - {}'.format(list_mismatched_type_cols))
    logger.info('column not found - {}'.format(list_columns_not_found))
    assert len(list_columns_not_found) == 0, 'columns missing from csv file - {}'.format(list_columns_not_found)
    assert len(list_mismatched_type_cols) == 0, 'columns mismatched type - {}'.format(list_mismatched_type_cols)


@pytest.mark.parametrize("input_csv_file_path, required_columns_list",
                         [('resources/csv/Customer_MR_NoDup.csv', ['FirstName', 'LastName', 'MemberNumber', 'SSN'])])
def test_TC_3_Validate_the_required_columns_in_the_input_csv_file(input_csv_file_path, required_columns_list):
    logger.info('expected required columns list - {}'.format(required_columns_list))
    input_file_columns_list = CsvHandler.get_csv_file_columns_list(input_csv_file_path)
    logger.info('columns present in input file - {}'.format(input_file_columns_list))
    assert all(col in input_file_columns_list for col in required_columns_list), \
        'All required columns not present in input csv!'


@pytest.mark.parametrize("input_csv_file_path, expected_no_of_rows",
                         [('resources/csv/Customer_MR_NoDup.csv', 50000)])
def test_TC_4_Validate_record_count_in_the_input_csv_file(input_csv_file_path, expected_no_of_rows):
    logger.info('expected number of rows in csv file - {}'.format(expected_no_of_rows))
    actual_rows_in_csv = CsvHandler.get_csv_file_row_count(input_csv_file_path, should_count_header=False)
    logger.info('actual number of rows in csv file - {}'.format(actual_rows_in_csv))
    assert actual_rows_in_csv == expected_no_of_rows, 'csv rows count mismatched!'


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_5_Validate_the_duplicate_records_in_the_input_csv_file(input_csv_file_path):
    logger.info('file under test - {}'.format(input_csv_file_path))
    count_duplicate_records = CsvHandler.get_duplicate_records_count(input_csv_file_path)
    logger.info('duplicate records count - {}'.format(count_duplicate_records))
    assert count_duplicate_records == 0, 'duplicate records found in csv!'


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_7_Validate_that_the_input_csv_file_is_not_empty(input_csv_file_path):
    logger.info('file under test - {}'.format(input_csv_file_path))
    row_count = CsvHandler.get_csv_file_row_count(input_csv_file_path, should_count_header=True)
    logger.info('is file empty - {}'.format(bool(row_count == 0)))
    assert row_count > 0, 'csv file is empty!'
