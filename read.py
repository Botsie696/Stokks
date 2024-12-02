import csv

# File paths
# input_file = "sorted_dictionary_output.txt"  # Replace with your text file name
# output_file = "output.csv"

# List to store parsed data
data = []
def StoreData(output_file , input_file):
# Read the input file
    with open(input_file, "r") as txt_file, open(output_file, "w", newline="") as csv_file:
        # Initialize CSV writer
        csv_writer = csv.writer(csv_file)
        
        # Read lines from the input file
        lines = txt_file.readlines()
        
        # Write the header (first line) as is
        header = lines[0].strip().split(",")  # Split by commas
        csv_writer.writerow(header)
        
        # Write the remaining lines
        for line in lines[1:]:  # Skip the header
            # Strip newline and split by commas
            row = line.strip().split(",")
            csv_writer.writerow(row)

    print(f"CSV file created at {output_file}") 
    print(f"Data has been written to {output_file}")

# import read2copy