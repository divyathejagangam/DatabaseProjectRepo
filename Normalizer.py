
def convert_to_1nf():

    return "No need to convert every relation is in 1NF, just has to create separate rows for non atomic values"


def convert_to_2nf(columns, functional_dependencies, composite_key):
    non_prime_attributes = set(columns) - set(composite_key)
    partial_dependencies = {}
    full_dependencies = {}
    for lhs, rhs in functional_dependencies.items():
        lhs_set = set((lhs,) if isinstance(lhs, str) else lhs)
        if lhs_set.issubset(composite_key) and lhs_set != set(composite_key):
            partial_dependencies[lhs] = rhs
        else:
            full_dependencies[lhs] = rhs
    new_relations = {}
    for lhs, rhs in partial_dependencies.items():
        lhs = (lhs,) if isinstance(lhs, str) else lhs
        table_name = '_'.join(lhs)
        new_columns = {attr.strip(): columns[attr] for attr in lhs + tuple(rhs)}
        new_relations[table_name] = {
            "columns": new_columns,
            "primary_key": list(lhs),
            "foreign_key": []
        }
        non_prime_attributes -= set(rhs)

    remaining_columns = {
        col: columns[col].strip() for col in columns if col in composite_key or col in non_prime_attributes}

    for lhs, rhs in full_dependencies.items():
        lhs = (lhs,) if isinstance(lhs, str) else lhs
        table_name = '_'.join(lhs)
        if table_name not in new_relations:
            new_relations[table_name] = {
                "columns": {attr.strip(): columns[attr] for attr in lhs},
                "primary_key": list(lhs),
                "foreign_key": []
            }
        for attr in rhs:
            new_relations[table_name]["columns"][attr.strip()] = columns[attr.strip()]
            if attr.strip() in remaining_columns:
                del remaining_columns[attr.strip()]

    new_relations["Main"] = {
        "columns": remaining_columns,
        "primary_key": composite_key,
        "foreign_key": {}
    }

    for lhs in partial_dependencies:
        lhs = (lhs,) if isinstance(lhs, str) else lhs
        for attr in lhs:
            if attr.strip() in composite_key:
                fk_name = '_'.join(lhs)
                new_relations["Main"]["foreign_key"][fk_name] = (
                    fk_name, fk_name)

    return new_relations



def convert_to_3nf(tables_2NF, functional_dependencies):
    new_tables = tables_2NF.copy()

    tables_to_check = list(new_tables.keys())

    while tables_to_check:
        table = tables_to_check.pop(0)
        columns = new_tables[table]['columns']
        primary_key = new_tables[table]['primary_key']

        non_prime_attributes = [
            col for col in columns.keys() if col not in primary_key]

        transitive_dependencies = {}
        for lhs, rhs_list in functional_dependencies.items():
            lhs = (lhs,) if isinstance(lhs, str) else lhs
            if set(lhs).issubset(set(non_prime_attributes)):
                for rhs in rhs_list:
                    if rhs in non_prime_attributes and rhs in columns:
                        transitive_dependencies[lhs] = rhs

        for lhs, rhs in transitive_dependencies.items():
            new_table_name = '{}_to_{}'.format('_'.join(lhs), rhs)
            new_tables[new_table_name] = {
                "columns": {attr: columns[attr] for attr in lhs + (rhs,)},
                "primary_key": list(lhs),
                "foreign_key": []
            }

            del new_tables[table]['columns'][rhs]

            if new_table_name not in tables_to_check:
                tables_to_check.append(new_table_name)
            new_tables[table]['foreign_key'].append(lhs)

    for table, details in new_tables.items():
        formatted_foreign_keys = {}
        for fk in details['foreign_key']:
            fk = '_'.join(fk) if isinstance(fk, tuple) else fk
            formatted_foreign_keys[fk] = (fk, fk)
        new_tables[table]['foreign_key'] = formatted_foreign_keys

    return new_tables


def convert_to_bcnf(tables_3NF, functional_dependencies):
    new_tables = tables_3NF.copy()

    moved_attributes = set()

    tables_to_check = list(new_tables.keys())

    while tables_to_check:
        table = tables_to_check.pop(0)
        columns = new_tables[table]['columns']
        primary_key = new_tables[table]['primary_key']

        violations = {}
        for lhs, rhs_list in functional_dependencies.items():
            lhs = (lhs,) if isinstance(lhs, str) else lhs
            if not set(lhs).issuperset(set(primary_key)) and not set(rhs_list).issubset(set(lhs)):
                for rhs in rhs_list:
                    if rhs in columns and lhs != (rhs,) and rhs not in moved_attributes:
                        violations[lhs] = violations.get(lhs, []) + [rhs]

        for lhs, rhs in violations.items():
            new_table_name = '{}_bcnf'.format('_'.join(lhs))
            new_columns = {attr: columns[attr]
                           for attr in lhs + tuple(rhs) if attr in columns}
            new_tables[new_table_name] = {
                "columns": new_columns,
                "primary_key": list(lhs),
                "foreign_key": []
            }

            for attr in rhs:
                if attr in new_tables[table]['columns']:
                    del new_tables[table]['columns'][attr]
                    moved_attributes.add(attr)

            if new_table_name not in tables_to_check:
                tables_to_check.append(new_table_name)
            new_tables[table]['foreign_key']['lhs'] = (lhs, lhs)

    for table, details in new_tables.items():
        formatted_foreign_keys = {}
        for fk in details['foreign_key']:
            fk = '_'.join(fk) if isinstance(fk, tuple) else fk
            formatted_foreign_keys[fk] = (fk, fk)
        new_tables[table]['foreign_key'] = formatted_foreign_keys

    return new_tables


def convert_to_4nf(bcnf_tables, multivalued_dependencies):
    new_tables = bcnf_tables.copy()

    # Find tables with multivalued dependencies
    mv_tables = []
    for table, details in bcnf_tables.items():
        if table in multivalued_dependencies:
            mv_tables.append(table)

    for mv_table in mv_tables:
        columns = new_tables[mv_table]['columns']
        primary_key = new_tables[mv_table]['primary_key']

        # Find the multivalued attributes
        mv_attributes = multivalued_dependencies[mv_table]

        # Create a new table for multivalued attributes
        mv_table_name = '{}_mv'.format(mv_table)
        mv_columns = {attr: columns[attr] for attr in mv_attributes}

        new_tables[mv_table_name] = {
            "columns": mv_columns,
            "primary_key": primary_key,
            "foreign_key": []
        }

        # Remove multivalued attributes from the original table
        for attr in mv_attributes:
            if attr in new_tables[mv_table]['columns']:
                del new_tables[mv_table]['columns'][attr]

    return new_tables
