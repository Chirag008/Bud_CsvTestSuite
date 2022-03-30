import xlrd
import pandas as pd


def get_column_name_to_column_type_mapping(schema_excel_file_path, source_type='CSV'):
    df = pd.read_excel(schema_excel_file_path)
    mapping = dict(df[df['Source'] == source_type][['Column Name', 'Column Type']].values)
    return {x.replace(' ', ''): v for x, v in mapping.items()}


if __name__ == '__main__':
    print(get_column_name_to_column_type_mapping('../resources/mappings/Customer File to Cunexus Mapping - Grouped.xlsx'))
