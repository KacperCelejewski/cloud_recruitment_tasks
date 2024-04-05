# Description: This is the main file for part 1 of the project. This file will be used to run the main code for part 1 of the project.
# Importing the required libraries
import csv
import sys
import os


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
    elif input_file == output_file:
        print("Error: Input and output file paths cannot be the same.")
        sys.exit(1)
    elif input_file.split(".")[-1] != "csv" or output_file.split(".")[-1] != "csv":
        print("Error: Please provide the path to the csv file.")
        sys.exit(1)
    elif not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist or is not a regular file.")
        sys.exit(1)
    elif not os.path.isfile(output_file):
        print(f"Error: File '{output_file}' does not exist or is not a regular file.")
        sys.exit(1)
    elif os.path.getsize(input_file) == 0:
        print(f"Error: File '{input_file}' is empty.")
        sys.exit(1)


if __name__ == "__main__":
    # Get the input and output file path
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # Validate the input arguments
    validate_file_arguments()
    # Open the input file
    sample_data = open_csv_file(input_file)
    # Write the output file
    write_csv_file(sys.argv[2], sample_data)
    print("Sample output file created successfully.")
