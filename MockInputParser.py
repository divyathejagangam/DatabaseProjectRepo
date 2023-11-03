def get_filename():
    return "/Users/pranaysinguluri/Stuff/DataBase/exampleInputTable.csv"


# def get_functional_dependencies():
#     return {
#         'StudentID': ['FirstName', 'LastName'],
#         'Course': ['CourseStart', 'CourseEnd', 'Professor'],
#         'Professor': ['ProfessorEmail']
#     }

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
def get_multivalued_dependencies_from_user():
    mv_fd_input = input("Enter multivalued functional dependencies (e.g., A->>B,C; X->>Y,Z; ...): ")

    # Split the input into individual multivalued dependencies using semicolons
    mv_fd_pairs = mv_fd_input.split(';')

    # Initialize a dictionary to store the multivalued functional dependencies
    multivalued_dependencies = {}

    for pair in mv_fd_pairs:
        pair = pair.strip()
        if '->' in pair:
            lhs, rhs = pair.split('->>', 1)  # Split only once
            lhs = lhs.strip()
            rhs = rhs.split(',')
            multivalued_dependencies[lhs] = rhs

    return multivalued_dependencies

# Example usage:
#multivalued_fd = get_multivalued_dependencies_from_user()


def get_composite_keys():
    composite_keys_input = input("Enter composite keys (e.g., ['StudentID', 'Course']): ")
    composite_keys = eval(composite_keys_input)  # Safely evaluate the input as a list
    return composite_keys
