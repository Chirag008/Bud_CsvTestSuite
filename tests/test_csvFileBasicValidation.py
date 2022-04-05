import pytest
import re
import logging
import src.CsvHandler as CsvHandler
import src.ExcelHandler as ExcelHandler
from src.ComparatorFunctions import ComparatorFunctions
from src.CustomLogger import CustomLogger, ResultType
from src.CsvHandler import ComparisonType
from src.Patterns import Patterns

logger = logging.getLogger(__name__)
c_logger = CustomLogger(logger)
patterns = Patterns()
cmp_funcs = ComparatorFunctions()


@pytest.fixture
def get_context():
    return {}


@pytest.mark.parametrize('input_csv_file_name',
                         ['Customer_MR_NoDup.csv'])
def test_TC_1_Validate_Excel_File_Naming_Convention(input_csv_file_name):
    csv_file_name_pattern = '.*.csv'
    c_logger.print('expected csv file pattern - {}'.format(csv_file_name_pattern), ResultType.EXPECTED)
    c_logger.print('Input csv file name - {}'.format(input_csv_file_name))
    file_name_matcher_regex = re.compile(csv_file_name_pattern)
    is_csv_name_as_per_standard = bool(file_name_matcher_regex.match(input_csv_file_name))
    c_logger.print('is csv name as per standard - {}'.format(is_csv_name_as_per_standard), ResultType.ACTUAL)
    assert is_csv_name_as_per_standard, 'input csv name not as per standards!'


@pytest.mark.parametrize('input_csv_file_path, schema_file_path',
                         [('resources/csv/Customer_MR_NoDup.csv',
                           'resources/mappings/Customer File to Cunexus Mapping - Grouped.xlsx')])
def test_TC_2_Validate_the_input_csv_file_schema(input_csv_file_path, schema_file_path):
    expected_col_name_to_type_mapping = ExcelHandler.get_column_name_to_column_type_mapping(schema_file_path)
    c_logger.print('Expected column name to column type - {}'.format(expected_col_name_to_type_mapping),
                   ResultType.EXPECTED)
    actual_col_name_to_type_mapping = CsvHandler.get_column_name_to_type_mappping(input_csv_file_path)
    c_logger.print('Actual column name to column type - {}'.format(actual_col_name_to_type_mapping), ResultType.ACTUAL)
    list_mismatched_type_cols = []
    list_columns_not_found = []
    for col, col_type in expected_col_name_to_type_mapping.items():
        if col not in actual_col_name_to_type_mapping.keys():
            list_columns_not_found.append(col)
        else:
            if actual_col_name_to_type_mapping[col] != col_type:
                list_mismatched_type_cols.append(col)
    c_logger.print('mismatched data type columns - {}'.format(list_mismatched_type_cols))
    c_logger.print('column not found - {}'.format(list_columns_not_found))
    assert len(list_columns_not_found) == 0, 'columns missing from csv file - {}'.format(list_columns_not_found)
    assert len(list_mismatched_type_cols) == 0, 'columns mismatched type - {}'.format(list_mismatched_type_cols)


@pytest.mark.parametrize("input_csv_file_path, required_columns_list",
                         [('resources/csv/Customer_MR_NoDup.csv', ['FirstName', 'LastName', 'MemberNumber', 'SSN'])])
def test_TC_3_Validate_the_required_columns_in_the_input_csv_file(input_csv_file_path, required_columns_list):
    c_logger.print('expected required columns list - {}'.format(required_columns_list), ResultType.EXPECTED)
    input_file_columns_list = CsvHandler.get_csv_file_columns_list(input_csv_file_path)
    c_logger.print('columns present in input file - {}'.format(input_file_columns_list), ResultType.ACTUAL)
    assert all(col in input_file_columns_list for col in required_columns_list), \
        'All required columns not present in input csv!'


@pytest.mark.parametrize("input_csv_file_path, expected_no_of_rows",
                         [('resources/csv/Customer_MR_NoDup.csv', 50000)])
def test_TC_4_Validate_record_count_in_the_input_csv_file(input_csv_file_path, expected_no_of_rows):
    c_logger.print('expected number of rows in csv file - {}'.format(expected_no_of_rows), ResultType.EXPECTED)
    actual_rows_in_csv = CsvHandler.get_csv_file_row_count(input_csv_file_path, should_count_header=False)
    c_logger.print('actual number of rows in csv file - {}'.format(actual_rows_in_csv), ResultType.ACTUAL)
    assert actual_rows_in_csv == expected_no_of_rows, 'csv rows count mismatched!'


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_5_Validate_the_duplicate_records_in_the_input_csv_file(input_csv_file_path):
    c_logger.print('file under test - {}'.format(input_csv_file_path))
    c_logger.print('expected duplicate records count - {}'.format(0), ResultType.EXPECTED)
    count_duplicate_records = CsvHandler.get_duplicate_records_count(input_csv_file_path)
    c_logger.print('duplicate records count - {}'.format(count_duplicate_records), ResultType.ACTUAL)
    assert count_duplicate_records == 0, 'duplicate records found in csv!'


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_7_Validate_that_the_input_csv_file_is_not_empty(input_csv_file_path):
    c_logger.print('file under test - {}'.format(input_csv_file_path))
    c_logger.print('File should not be empty', ResultType.EXPECTED)
    row_count = CsvHandler.get_csv_file_row_count(input_csv_file_path, should_count_header=True)
    c_logger.print('is file empty - {}'.format(bool(row_count == 0)), ResultType.ACTUAL)
    assert row_count > 0, 'csv file is empty!'


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_8_Validate_the_MasterAccount_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'MasterAccount'
    pattern = patterns.boolean
    expectation = 'MasterAccount field should be populated with one of the Boolean format values 0 or 1 or converted'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_9_Validate_the_State_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'State'
    pattern = r'^[A-Z]{2}$'
    expectation = 'State field should be populated with a valid 2-character state value'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_10_Validate_the_ZipCodePrefix_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'ZipCodePrefix'
    pattern = r'^[\d]{5}$'
    expectation = 'ZipCodePrefix field should be populated with the first 5 numbers of a customer’s zip code value'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_11_Validate_the_ZipCodeSuffix_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'ZipCodePrefix'
    pattern = r'^[\d]{4}$'
    expectation = 'ZipCodeSuffix field should be populated with the last 4 numbers of a customer’s zip code value'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_12_Validate_the_BirthDate_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'BirthDate'
    pattern = patterns.date
    expectation = 'BirthDate field should be populated or converted to a valid date format MM/DD/YYYY'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_13_Validate_the_EmailAddress_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'EmailAddress'
    pattern = patterns.email
    expectation = 'EmailAddress field should be populated with a standard email address format: {prefix}@{domain}.com'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_14_Validate_the_SSN_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'SSN'
    pattern = r'^[0-9]{9}$'
    expectation = 'SSN field should be populated with the format ######### (9 digits)'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_15_Validate_the_Income_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'Income'
    pattern = patterns.number_or_decimal
    expectation = 'Income field should be populated with a numeric format with or without decimals'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_17_Validate_the_EmploymentDate_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'EmploymentDate'
    pattern = patterns.date
    expectation = 'EmploymentDate field should be populated or converted to a valid date format MM/DD/YYYY'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_19_Validate_the_MemberStartDate_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'MemberStartDate'
    pattern = patterns.date
    expectation = 'MemberStartDate  field should be populated or converted to a valid date format MM/DD/YYYY'
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_20_Validate_the_SavingsAccountFlag_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'SavingsAccountFlag'
    pattern = patterns.boolean
    expectation = 'SavingsAccountFlag field should be populated with one of the Boolean format values 0 or 1 or ' \
                  'converted to it '
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_21_Validate_the_CheckingFlag_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'CheckingFlag'
    pattern = patterns.boolean
    expectation = 'CheckingFlag field should be populated with one of the Boolean format values 0 or 1 or converted ' \
                  'to it '
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_22_Validate_the_CDFlag_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'CDFlag'
    pattern = patterns.boolean
    expectation = 'CDFlag field should be populated with one of the Boolean format values 0 or 1 or converted ' \
                  'to it '
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_23_Validate_the_MoneyMarketFlag_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'MoneyMarketFlag'
    pattern = patterns.boolean
    expectation = 'MoneyMarketFlag field should be populated with one of the Boolean format values 0 or 1 or converted ' \
                  'to it '
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


@pytest.mark.parametrize('input_csv_file_path',
                         ['resources/csv/Customer_MR_NoDup.csv'])
def test_TC_24_Validate_the_AutoLoanFlag_field_in_the_input_csv_file(input_csv_file_path):
    col_name = 'AutoLoanFlag'
    pattern = patterns.boolean
    expectation = 'AutoLoanFlag field should be populated with one of the Boolean format values 0 or 1 or converted ' \
                  'to it '
    validate_column_value_as_per_standards(input_csv_file_path, col_name, ComparisonType.REGEX, pattern, expectation)


def validate_column_value_as_per_standards(input_csv_file_path, col_name, c_type: ComparisonType, comparator,
                                           expectation):
    c_logger.print(f'{expectation}', ResultType.EXPECTED)
    try:
        list_values_not_following_condition = []
        if c_type == ComparisonType.REGEX:
            list_values_not_following_condition = CsvHandler.get_list_values_not_following_regex(input_csv_file_path,
                                                                                                 col_name,
                                                                                                 comparator)
        elif c_type == ComparisonType.FUNCTION:
            list_values_not_following_condition = CsvHandler.get_list_values_not_following_condition(
                input_csv_file_path,
                col_name,
                comparator)
        else:
            raise Exception(f'{c_type} has not been implemented yet!')

        if len(list_values_not_following_condition) == 0:
            c_logger.print(f'{col_name} field value is following the pattern', ResultType.ACTUAL)
        else:
            c_logger.print(f'No of rows not matching the expected pattern - {len(list_values_not_following_condition)}.'
                           f'\nFirst few values not matching the pattern - {list_values_not_following_condition[:10]}',
                           ResultType.ACTUAL)
        assert len(list_values_not_following_condition) == 0, f'all values in field {col_name} not following pattern'
    except KeyError as e:
        c_logger.print(f'{col_name} not present in input csv file', ResultType.ACTUAL)
        raise e
