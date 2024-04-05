# Description: This is the main file for part 1 of the project. This file will be used to run the main code for part 1 of the project.
# Importing the required libraries
import csv
import sys


# Open given csv file
def open_csv_file(file_path):
    """Open the given csv file and return the data as a list of lists."""
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found or cannot be opened.")
        return None
    except Exception as e:
        print("Error: ", e)
        return None


def write_csv_file(file_path, data):
    """Write the given data to the given csv file."""
    try:
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found or cannot be opened.")
    except Exception as e:
        print("Error: ", e)


def validate_file_arguments():
    """Validate the input arguments provided by the user."""
    # Check if the input and output file path is provided
    if len(sys.argv) != 3:
        print(
            "Error: Please provide the path to the input and output csv file. \nUsage: python main.py <input_file_path> <output_file_path>"
        )
        sys.exit(1)
    # Check if the input and output file path is valid
    elif sys.argv[1] == sys.argv[2]:
        print("Error: Input and output file paths cannot be the same.")
        sys.exit(1)
    elif sys.argv[1].split(".")[-1] != "csv" or sys.argv[2].split(".")[-1] != "csv":
        print("Error: Please provide the path to the csv file.")
        sys.exit(1)


if __name__ == "__main__":
    # Validate the input arguments
    validate_file_arguments()
    # Open the input file
    sample_data = open_csv_file(sys.argv[1])
    # Write the output file
    write_csv_file(sys.argv[2], sample_data)
    print("Sample output file created successfully.")
