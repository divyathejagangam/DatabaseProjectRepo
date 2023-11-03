
import csv
from datetime import datetime


def get_columns(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        sample_data = [next(csv_reader) for _ in range(2)]

    column_datatypes = {}
    for i, column_name in enumerate(header):
        datatype = None
        for row in sample_data:
            try:
                _ = int(row[i])
                datatype = 'INT'
                break
            except ValueError:
                try:
                    _ = float(row[i])
                    datatype = 'FLOAT'
                    break
                except ValueError:
                    try:
                        datetime.strptime(row[i], "%d/%m/%y")
                        datatype = 'DATE'
                    except ValueError:
                        if len(row[i]) <= 255:
                            datatype = f'VARCHAR(255)'
                        else:
                            datatype = 'TEXT'

        column_datatypes[column_name] = datatype

    return column_datatypes


def generate_table_command(table_name, columns, primary_key=None, foreign_keys=None):
    cmd = f"CREATE TABLE {table_name} (\n"

    for column, data_type in columns.items():
        cmd += f"{column} {data_type}"
        if primary_key and column == primary_key:
            cmd += " PRIMARY KEY"
        cmd += ",\n"

    if foreign_keys:
        for fk_column, (ref_table, ref_column) in foreign_keys.items():
            cmd += f"FOREIGN KEY ({fk_column}) REFERENCES {ref_table}({ref_column}),\n"

    cmd = cmd.rstrip(',\n')
    cmd += "\n);"
    return cmd


def print_1nf_commands(table_name, columns):
    print("SQL queries to create 1NF:")
    table_1nf = generate_table_command(table_name, columns)
    print(table_1nf)


def print_nf_commands(output_2nf):
    print("SQL queries to create Queries:")
    for table_name, details in output_2nf.items():
        query = generate_table_command(
            table_name, details['columns'], details['primary_key'][0], details['foreign_key'])
        print(query)


# def print_3nf_commands(output_3nf):
#     print("SQL queries to create 3NF:")
#     for table_name, details in output_3nf.items():
#         query = generate_table_command(
#             table_name, details['columns'], details['primary_key'][0], details['foreign_key'])
#         print(query)

# def print_bcnf_commands(output_bnf):
#     print("SQL queries to create BCNF:")
#     for table_name, details in output_bnf.items():
#         query = generate_table_command(
#             table_name, details['columns'], details['primary_key'][0], details['foreign_key'])
#         print(query)
