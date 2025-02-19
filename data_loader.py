# Load the data from the text files 

file_paths = ["data/sppnw41.txt", "data/sppnw42.txt", "data/sppnw43.txt"]

def load_data(file_path):
    with open(file_path, 'r') as file:
        # Read the number of rows and columns
        num_rows, num_columns = map(int, file.readline().strip().split())

        # Initialize a list to store column data
        columns = []

        # Read each column's data
        for _ in range(num_columns):
            # Read the column cost and number of rows covered
            column_cost, num_rows_covered, *rows_covered = map(int, file.readline().strip().split())

            # Append the column data as a tuple to the columns list
            columns.append((column_cost, num_rows_covered, rows_covered))

    return num_rows, num_columns, columns 




# # Test the load_data function
# if __name__ == "__main__":
#     num_rows, num_columns, columns = load_data("data/sppnw41.txt")
#     print(f"Number of rows: {num_rows}")
#     print(f"Number of columns: {num_columns}")
#     print(f"Columns: {columns}")
