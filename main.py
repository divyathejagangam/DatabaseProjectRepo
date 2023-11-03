from Normalizer import convert_to_1nf, convert_to_2nf, convert_to_3nf, convert_to_4nf, convert_to_bcnf
from NormalFormFinder import is_in_1NF, is_in_2NF, is_in_3nf
from MockInputParser import get_functional_dependencies_from_user, get_multivalued_dependencies_from_user
from SQLQueryGenerator import get_columns, print_1nf_commands, print_nf_commands

def main():
    # Get input from the user
    file_name = input("Enter the file path: ")
    functional_dependencies = get_functional_dependencies_from_user()
    multivalued_dependencies = get_multivalued_dependencies_from_user()
    composite_keys_input = input("Enter composite keys (comma-separated, e.g., StudentID,CourseID): ")
    composite_keys = composite_keys_input.split(',')
    normalization_form = input("Enter the desired normalization form (1NF, 2NF, 3NF, BCNF, 4NF, 5NF): ")

    # Get columns from the file
    columns = get_columns(file_name)

    if normalization_form == "1":
        print("Is in 1NF: ", is_in_1NF(file_name))
        print_1nf_commands("Student", columns)
        convert_to_1nf()
    elif normalization_form == "2":
        print("Is in 2NF: ", is_in_2NF(columns, functional_dependencies, composite_keys))
        results_2nf = convert_to_2nf(columns, functional_dependencies, composite_keys)
        print_nf_commands(results_2nf)
    elif normalization_form == "3":
        results_2nf = convert_to_2nf(columns, functional_dependencies, composite_keys)
        results_3nf = convert_to_3nf(results_2nf, functional_dependencies)
        print_nf_commands(results_3nf)
    elif normalization_form == "B":
        results_2nf = convert_to_2nf(columns, functional_dependencies, composite_keys)
        results_3nf = convert_to_3nf(results_2nf, functional_dependencies)
        results_bcnf = convert_to_bcnf(results_3nf, functional_dependencies)
        print_nf_commands(results_bcnf)
    # elif normalization_form == "4":
    #     results_2nf = convert_to_2nf(columns, functional_dependencies, composite_keys)
    #     results_3nf = convert_to_3nf(results_2nf, functional_dependencies)
    #     results_bcnf = convert_to_bcnf(results_3nf, functional_dependencies)
    #     new_4nf_tables = convert_to_4nf(results_bcnf, multivalued_dependencies)
    #     print_nf_commands(new_4nf_tables)

    # elif normalization_form == "5NF":
    #     results_2nf = convert_to_2nf(columns, functional_dependencies, composite_keys)
    #     results_3nf = convert_to_3nf(results_2nf, functional_dependencies)
    #     results_bcnf = convert_to_bcnf(results_3nf, functional_dependencies)
    #     print_3nf_commands(results_bcnf)
        
    else:
        print("Invalid normalization form specified. Please choose 1NF, 2NF, 3NF, or BCNF.")

if __name__ == "__main__":
    main()
