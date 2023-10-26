
import csv

# Function to read a CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

#Extract columns with missing values
def extract_columns_with_missing_values(data):
    columns_with_missing_values = []
    for i in range(len(data[0])):
        column_values = [row[i] for row in data]
        if None in column_values or '' in column_values:
            columns_with_missing_values.append(i)
    return columns_with_missing_values

# Count the number of lines with missing data
def count_lines_with_missing_data(data):
    count = 0
    column_missing_values = extract_columns_with_missing_values(data)
    for i in range(len(data)):
        row_values = [row for row in data[i]]
        for j in range(len(column_missing_values)):
            number_column = column_missing_values[j]
            if '' in row_values[number_column]:
                count += 1
                break
            
    return count

#Fill in the missing value using mean, median (for numeric properties) and mode (for the categorical attribute).
def fill_in_missing_values(data, method, columns):
    for i in columns:
        if method == "mean":
            valid_data = [float(row[i]) for row in data if row[i] is not None or '']
            mean_value = sum(valid_data) / len(valid_data)
            for row in data:
                if row[i] is None:
                    row[i] = mean_value
        elif method == "median":
            valid_data = [float(row[i]) for row in data if row[i] is not None or '']
            valid_data.sort()
            median_value = valid_data[len(valid_data) // 2]
            for row in data:
                if row[i] is None:
                    row[i] = median_value
        elif method == "mode":
            valid_data = [row[i] for row in data if row[i] is not None or '']
            count = {}
            max_count = 0
            mode_value = None
            for value in valid_data:
                count[value] = count.get(value, 0) + 1
                if count[value] > max_count:
                    max_count = count[value]
                    mode_value = value
            for row in data:
                if row[i] is None:
                    row[i] = mode_value
        else:
            print(f"Unknown method: {method}")
            return None

    return data

#Deleting columns containing more than a particular number of missing values 
def delete_column(data, number):
    for i in range (data[0].length):
        valid_data = [row[i] for row in data if row[i] is not None or '']
def main():
    file_path = 'house-prices.csv'
    data = read_csv(file_path)

    # Extract columns with missing values
    columns_with_missing = extract_columns_with_missing_values(data)
    print("Columns with missing values:", columns_with_missing)

    # Count the number of lines with missing data
    number_of_lines_missing_data = count_lines_with_missing_data(data)
    print("Numbers of lines with missing data: ", number_of_lines_missing_data)
    # Fill in missing values using mean, median, or mode
    
    

if __name__ == "__main__":
    main()
