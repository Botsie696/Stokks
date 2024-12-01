import csv

def read_csv_to_dict(file_path):
    """Reads a CSV file into a dictionary with the first column as the key."""
    data_dict = {}
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read headers
            for row in reader:
                if row:  # Skip empty rows
                    data_dict[row[0]] = row[1:]  # Use the first column as the key
    except FileNotFoundError:
        print(f"{file_path} not found. Creating a new file.")
    return data_dict, headers if 'headers' in locals() else None

def write_dict_to_csv(file_path, data_dict, headers):
    """Writes a dictionary to a CSV file."""
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        for key, values in data_dict.items():
            writer.writerow([key] + values)  # Write key and associated values

def merge_csv_files(file1_path, file2_path  , newFile):
    """
    Merges file1 into file2:
    - Rows from file1 overwrite rows in file2 if the key exists in both.
    - Rows unique to file2 remain.
    """
    # Read data from both files
    file1_data, file1_headers = read_csv_to_dict(file1_path)
    file2_data, file2_headers = read_csv_to_dict(file2_path)

    # Ensure headers match; if not, align them
    if file1_headers != file2_headers:
        raise ValueError("Headers of the two files do not match.")

    # Merge file1 into file2
    merged_data = file2_data.copy()  # Start with all rows from file2
    merged_data.update(file1_data)  # Overwrite/add rows from file1

    # Write the merged data back to file2
    write_dict_to_csv(newFile, merged_data, file2_headers)
    print(f"Merged data written to {newFile}")

# File paths
input_file = "sorted_dictionary_output.txt"  # File to append
output_file = "outputnew.csv"  # Existing file

# Convert the text input file to a CSV-compatible format (if needed)
with open(input_file, "r") as txt_file, open("temp.csv", "w", newline="") as temp_csv:
    csv_writer = csv.writer(temp_csv)
    lines = txt_file.readlines()
    headers = lines[0].strip().split(",")
    csv_writer.writerow(headers)
    for line in lines[1:]:
        row = line.strip().split(",")
        csv_writer.writerow(row)

# Merge temp.csv (converted input file) into output.csv
merge_csv_files("temp.csv", output_file  , "outputnew.csv")
