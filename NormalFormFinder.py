import csv


def read_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def is_atomic(value):
    if isinstance(value, str) and ',' in value:
        return False
    return not isinstance(value, (list, set, tuple, dict))


def is_in_1NF(file_path):
    data = read_from_csv(file_path)
    if len(data) != len(set(tuple(row.items()) for row in data)):
        return False

    for column in data[0].keys():
        if not all(is_atomic(row[column]) for row in data):
            return False

        types_in_column = {type(row[column]) for row in data}
        if len(types_in_column) > 1:
            return False

    return True


def is_in_2NF(columns, functional_dependencies, composite_key):
    non_prime_attributes = [col for col in columns if col not in composite_key]
    for lhs, rhs in functional_dependencies.items():
        if set([lhs]).issubset(composite_key) and not set([lhs]) == set(composite_key):
            for attr in rhs:
                if attr in non_prime_attributes:
                    return False

    return True


def is_in_3nf(tables, functional_dependencies):
    all_columns = set()
    for table_details in tables.values():
        all_columns.update(table_details['columns'].keys())

    for lhs, rhs_list in functional_dependencies.items():
        if lhs not in all_columns:
            return False
        for rhs in rhs_list:
            if rhs not in all_columns:
                return False

    for table, details in tables.items():
        primary_key = details['primary_key']
        non_prime_attributes = [
            col for col in details['columns'] if col not in primary_key]

        for lhs, rhs_list in functional_dependencies.items():
            if lhs in non_prime_attributes:
                for rhs in rhs_list:
                    if rhs in non_prime_attributes:
                        for pk in primary_key:
                            if pk in functional_dependencies and lhs in functional_dependencies[pk]:
                                return False

    return True
def is_in_bcnf(tables, functional_dependencies):
    all_columns = set()
    for table_details in tables.values():
        all_columns.update(table_details['columns'].keys())

    for lhs, rhs_list in functional_dependencies.items():
        if lhs not in all_columns:
            return False
        for rhs in rhs_list:
            if rhs not in all_columns:
                return False

    for table, details in tables.items():
        primary_key = details['primary_key']
        non_prime_attributes = [
            col for col in details['columns'] if col not in primary_key]

        for lhs, rhs_list in functional_dependencies.items():
            if lhs in non_prime_attributes:
                for rhs in rhs_list:
                    if rhs in non_prime_attributes:
                        for pk in primary_key:
                            if pk in functional_dependencies and lhs in functional_dependencies[pk]:
                                return False

        # Check BCNF condition
        for lhs, rhs_list in functional_dependencies.items():
            for rhs in rhs_list:
                if lhs != primary_key and not is_superkey(lhs, primary_key, functional_dependencies):
                    return False

    return True

def is_superkey(X, candidate_key, functional_dependencies):
    # Check if X is a superkey based on candidate_key
    if X == candidate_key:
        return True

    # Check if X is a superkey based on functional dependencies
    if X in candidate_key:
        return True

    for lhs, rhs_list in functional_dependencies.items():
        for rhs in rhs_list:
            if set(lhs).issubset(set(X)) and not set(rhs).issubset(set(X)):
                return False

    return True
