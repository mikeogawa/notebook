import csv


def read_csv(file_path):
    dict_list = []
    
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        # Create a CSV DictReader object
        csv_reader = csv.DictReader(file)
        
        # Iterate over each row and add it to the list
        for row in csv_reader:
            dict_list.append(dict(row))
    
    return dict_list