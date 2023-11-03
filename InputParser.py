def get_filename():
    return input()


def get_functional_dependencies_from_user():
    fd_input = input("Enter functional dependencies (e.g., StudentID->FirstName,LastName;Course->CourseStart,CourseEnd,Professor;...): ")

    # Split the input into individual dependencies using semicolons
    fd_pairs = fd_input.split(';')

    # Initialize an empty dictionary to store the functional dependencies
    functional_dependencies = {}

    for pair in fd_pairs:
        pair = pair.strip()
        if '->' in pair:
            lhs, rhs = pair.split('->', 1)  # Split only once
            lhs = lhs.strip()
            rhs = rhs.split(',')
            functional_dependencies[lhs] = rhs

    return functional_dependencies



def get_composite_keys():
    values = input()
    return [value.strip()
            for value in values.split(",")]
