# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file
import csv, os, copy


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def reader(csv_file_name):
    list = []
    with open(os.path.join(__location__, csv_file_name)) as a:
        rows = csv.DictReader(a)
        for r in rows:
            list.append(dict(r))
    return list


def writer(csv_file_name,list,row_list):
    myFile = open(csv_file_name, 'w')
    writer = csv.writer(myFile)
    writer.writerow(row_list)
    for dictionary in list:
        writer.writerow(dictionary.values())
    myFile.close()


# add in code for a Database class
class Database:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table


# # add in code for a Table class
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table


    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table


    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table


    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)


    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps


    def __str__(self):
        return str(self.table)


# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
    def insert_row(self, dict):
        self.table.append(dict)


# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
    def update_row(self, primary_attribute, primary_attribute_value, update_attribute, update_value):
        for i in self.table:
            if i[primary_attribute] == primary_attribute_value:
                i[update_attribute] = update_value