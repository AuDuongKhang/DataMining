import sys
import csv

# Function to read a CSV file


def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Function to write CSV file


def export_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

# Extract columns with missing values


def extract_columns_with_missing_values(data):
    columns_with_missing_values = []
    column_missing_count = []
    for i in range(len(data[0])):
        column_values = [row[i] for row in data]
        missing_count = column_values.count(None) + column_values.count('')
        if missing_count > 0:
            columns_with_missing_values.append(i)
            column_missing_count.append(missing_count)

    return columns_with_missing_values, column_missing_count

# Count the number of lines with missing data


def count_lines_with_missing_data(data):
    matrix = data.copy()
    del matrix[0]
    count = 0
    column_missing_values, column_missing_count = extract_columns_with_missing_values(
        matrix)
    for i in range(len(matrix)):
        row_values = [row for row in matrix[i]]
        for j in range(len(column_missing_values)):
            number_column = column_missing_values[j]
            if row_values[number_column] == '':
                count += 1
                break

    return count


def calculate_mean(column):
    numeric_values = [x for x in column if isinstance(x, (int, float))]
    if not numeric_values:
        raise ValueError("Column contains no numeric values")
    return sum(numeric_values) / len(numeric_values)


def calculate_standard_deviation(column):
    numeric_values = [x for x in column if isinstance(x, (int, float))]
    if not numeric_values:
        raise ValueError("Column contains no numeric values")

    mean = calculate_mean(numeric_values)
    variance = sum((x - mean) ** 2 for x in numeric_values) / \
        len(numeric_values)
    return variance ** 0.5


def calculate_mode(data):
    count = {}
    max_count = 0
    mode_value = None
    for value in data:
        count[value] = count.get(value, 0) + 1
        if count[value] > max_count:
            max_count = count[value]
            mode_value = value
    return mode_value


def calculate_median(data):
    data.sort()
    if len(data) % 2 == 0:
        return (data[len(data) // 2] + data[len(data) // 2 - 1]) / 2
    else:
        return data[len(data) // 2]

# Fill in the missing value using mean, median (for numeric properties) and mode (for the categorical attribute).


def fill_in_missing_values(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] is None or data[i][j] == '':
                column_values = [row[j]
                                 for row in data if row[j] is not None and row[j] != '']
                if len(column_values) == 0:
                    continue  # Skip if all values in the column are missing
                if isinstance(column_values[0], (float, int)):
                    data[i][j] = calculate_median(column_values)
                else:
                    data[i][j] = calculate_mode(column_values)
    return data


# Deleting rows containing more than a particular number of missing values


def delete_row_has_more_than_particular_num(data, num):
    matrix = data.copy()  # create a copy of the data
    del matrix[0]         # delete first row of data
    particular_num = num * len(data[0]) / 100
    column_missing_values, column_missing_count = extract_columns_with_missing_values(
        data)

    i = 0
    while i < len(matrix):
        count = 0
        row_values = [row for row in matrix[i]]
        for j in range(len(column_missing_values)):
            number_column = column_missing_values[j]
            if row_values[number_column] == '':
                count += 1

        if count >= particular_num:
            del matrix[i]
        else:
            i += 1

    return matrix

# Delete duplicate samples.


def delete_column_has_more_than_particular_num(data, num):
    matrix = data.copy()
    particular_num = num * len(data) / 100
    i = 0
    while i < len(matrix[0]):
        column_values = [row[i] for row in matrix]
        count = column_values.count('') + column_values.count(None)
        if count >= particular_num:
            for row in matrix:
                del row[i]
        else:
            i += 1
    return matrix


def delete_duplicate(data):
    matrix = data.copy()
    del matrix[0]
    i = 0
    while i < len(matrix):
        row_values_i = [row for row in matrix[i]]
        j = i + 1
        while j < len(matrix):
            row_values_j = [row for row in matrix[j]]
            if row_values_i == row_values_j:
                del matrix[j]
            else:
                j += 1
        i += 1
    return matrix

# Performing addition, subtractionion, multiplication, and division between two numerical attributes.

# Get all numeric attributes


def get_numeric_attributes(data):
    data_set = data.copy()
    del data_set[0]
    numeric_attributes = []
    for i in range(len(data[0])):
        column_values = [row[i] for row in data]
        for j in range(len(column_values)):
            try:
                float(column_values[j])
                numeric_attributes.append(i)
                break
            except ValueError:
                continue

    return numeric_attributes


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def normalize_numeric_attribute(data, method, column_name):
    num_rows = len(data)
    header = data[0]
    column_name_to_index = {name: index for index, name in enumerate(header)}
    column_index = column_name_to_index.get(column_name)
    if column_index is None:
        raise ValueError(
            f"Column name '{column_name}' not found in the header.")
    # Check if all values in the column are numeric

    column = [row[column_index] for row in data[1:]]
    if not all(is_numeric(val) for val in column):
        raise ValueError(f"Non-numeric values found in column '{column_name}'")
    column = [float(row[column_index])
              for row in data[1:]]  # Convert values to float

    if method == 'min-max':
        min_value = min(column)
        max_value = max(column)
        for i in range(1, num_rows):
            data[i][column_index] = (
                float(data[i][column_index]) - min_value) / (max_value - min_value)
    elif method == 'z-score':
        mean = sum(column) / len(column)
        variance = sum((x - mean) ** 2 for x in column) / len(column)
        std_dev = variance ** 0.5
        for i in range(1, num_rows):
            data[i][column_index] = (
                float(data[i][column_index]) - mean) / std_dev
    else:
        raise ValueError('Invalid method')

    return data


def is_operator(operation):
    if operation == 'addition' or operation == 'subtraction' or operation == 'multiplication' or operation == 'division':
        return True
    else:
        return False

# Handle calculation


def handle_calculation(data, attr_1, attr_2, operation):
    data_set = data.copy()
    del data_set[0]
    numeric_attributes = get_numeric_attributes(data)
    results = []
    for row in data_set:
        if (is_operator(operation) and attr_1 in numeric_attributes and attr_2 in numeric_attributes):
            if operation == 'addition':
                result = float(row[attr_1]) + float(row[attr_2])
            elif operation == 'subtraction':
                result = float(row[attr_1]) - float(row[attr_2])
            elif operation == 'multiplication':
                result = float(row[attr_1]) * float(row[attr_2])
            elif operation == 'division':
                result = float(row[attr_1]) / float(row[attr_2])

            results.append(result)  # Wrap result in a list
        else:
            if is_operator(operation) == False:
                print(f"Unknow operation: {operation}")
                return
            elif attr_1 not in numeric_attributes or attr_2 not in numeric_attributes:
                print(f"Attribute 1 or attribute 2 is not numeric attributes")
                return

    return results


def main():
    file_path = str(sys.argv[1]).split("=")[1]
    input_function = str(sys.argv[2]).split("=")[1]
    output_file = str(sys.argv[len(sys.argv)-1].split("=")[1])

    data = read_csv(file_path)

    # Extract columns with missing values
    # cmdline: python3 lab01.py file_path=house-prices.csv function=extract_columns_with_missing_values
    if input_function == 'extract_columns_with_missing_values':
        columns_with_missing, column_missing_count = extract_columns_with_missing_values(
            data)
        print("Columns with missing values:")
        for i in range(len(column_missing_count)):
            column_name = f"{data[0][columns_with_missing[i]]}"
            print(column_name, "-", column_missing_count[i], "missing values")

    # Count the number of lines with missing data
    # cmdline: python3 lab01.py file_path=house-prices.csv function=count_lines_with_missing_data
    if input_function == 'count_lines_with_missing_data':
        number_of_lines_missing_data = count_lines_with_missing_data(data)
        print("Numbers of lines with missing data: ",
              number_of_lines_missing_data)

    # Fill in missing values using mean, median, or mode
    # cmdline: python3 lab01.py file_path=house-prices.csv function=fill_in_missing_values output_file=q3.csv
    if input_function == 'fill_in_missing_values':
        data_after_be_filled = fill_in_missing_values(data)
        export_to_csv(data_after_be_filled, output_file)

    # Deleting rows containing more than a particular number of missing values
    # cmdline: python3 lab01.py file_path=house-prices.csv function=delete_row_has_more_than_particular_num particular_num=10 output_file=q4.csv

    if input_function == 'delete_row_has_more_than_particular_num':
        particular_num = str(sys.argv[3]).split("=")[1]
        matrix = delete_row_has_more_than_particular_num(
            data, int(particular_num))
        print("Length of matrix after deleting rows have more than particular number with missing values:", len(matrix))
        export_to_csv(matrix, output_file)

    # Deleting columns containing more than a particular number of missing values
    # cmdline: python3 lab01.py file_path=house-prices.csv function=delete_column_has_more_than_particular_num particular_num=10 output_file=q5.csv

    if input_function == 'delete_column_has_more_than_particular_num':
        particular_num = str(sys.argv[3]).split("=")[1]
        matrix = delete_column_has_more_than_particular_num(
            data, int(particular_num))
        print("Deleted!")
        export_to_csv(matrix, output_file)

    # Delete duplicate samples.
    # cmdline: python3 lab01.py file_path=house-prices.csv function=delete_duplicate output_file=q6.csv

    if input_function == 'delete_duplicate':
        matrix = delete_duplicate(data)
        print("Data after delete dupplicates samples:", len(matrix))
        export_to_csv(matrix, output_file)

    # Normalize a numeric attribute using min-max and Z-score methods.
    # cmdline: python3 lab01.py file_path=house-prices.csv function=normalize_numeric_attribute method=z-score output_file=q7.csv
    if input_function == 'normalize_numeric_attribute':
        method = str(sys.argv[3]).split("=")[1]
        col_name = str(sys.argv[4]).split("=")[1]
        normalize_data = normalize_numeric_attribute(data, method, col_name)
        export_to_csv(normalize_data, output_file)

    # Performing addition, subtractionion, multiplication, and division between two numerical attributes.
    # cmdline: python3 lab01.py file_path=house-prices.csv function=handle_calculation attr_1=Id attr_2=MSSubClass operation=addition output_file=q8.csv

    if input_function == 'handle_calculation':
        results = []
        attr_1 = str(sys.argv[3]).split("=")[1]
        attr_2 = str(sys.argv[4]).split("=")[1]
        operation = str(sys.argv[5]).split("=")[1]
        for i in range(len(data[0])):
            if attr_1 == data[0][i]:
                attr_1 = i
            elif attr_2 == data[0][i]:
                attr_2 = i
        calculation = handle_calculation(data, attr_1, attr_2, operation)
        results.append([data[0][attr_1], data[0][attr_2], operation])
        for i in range(len(calculation)):
            results.append(
                [data[i+1][attr_1], data[i+1][attr_2], calculation[i]])
        export_to_csv(results, output_file)


if __name__ == "__main__":
    # Example usage
    main()
