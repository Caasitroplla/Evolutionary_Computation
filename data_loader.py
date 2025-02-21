import random
# Load the data from the text files 

file_paths = ["data/sppnw41.txt", "data/sppnw42.txt", "data/sppnw43.txt"]

def _load_data(file_path):
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


def load_attendants(file_path = file_paths[0]):
    data = _load_data(file_path)
    # The data is in the format (num_rows, num_columns, columns)
    # Each column contains (column_cost, num_rows_covered, rows_covered)
    
    columns = data[2]  # Access the third element of the tuple
 
    attendants = {}
    for i, column_data in enumerate(columns):
        # Generate crew IDs as 'AA', 'AB', 'AC', ..., 'BA', 'BB', etc.
        first_letter = chr(65 + (i // 26))  # A, B, C, etc.
        second_letter = chr(65 + (i % 26))  # A, B, C, etc.
        crew = first_letter + second_letter
        
        cost = column_data[0]
        flights = column_data[2]
        attendants[crew] = {'cost': cost, 'flights': flights}

    return attendants

def load_flights(file_path = file_paths[0]):
    data = _load_data(file_path)
    # The first item is the number of rows and columns we want to return then number if rows
    return data[0]

def get_random_dataset():
    random_file_path = random.choice(file_paths)
    attendants = load_attendants(random_file_path)
    flights = load_flights(random_file_path)
    return attendants, flights





# Test the load_data function

# if __name__ == "__main__":
#     num_rows, num_columns, columns = _load_data("data/sppnw41.txt")
#     print(f"Number of rows: {num_rows}")
#     print(f"Number of columns: {num_columns}")
#     print(f"Columns: {columns}")

#     attendants = load_attendants()
#     print(f"Attendants: {attendants}")

#     flights = load_flights()
#     print(f"Flights: {flights}")
