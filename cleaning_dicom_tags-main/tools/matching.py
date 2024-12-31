import csv

class Matching:

    def read_table(matching_csv_path):
    
        match_dict = {}
        with open(matching_csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            for row in csvreader:
                if len(row)>0:
                    match_dict[row[0]] = row[1] 
        return match_dict

