import os
import csv
import pymongo
from pymongo import MongoClient
import json

def create_database(client): # creating db
    database = client['User_Information_test_1']
    return database

def create_collection(database, collection_name): # creating collection
    collection = database[collection_name]
    return collection

def insert_data(collection, csv_file_path):  # function to insert data into the database by reading the csv files
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            collection.insert_one(row)

def create_indexes_from_json(database, json_file_path): # function to create indexes from the information given in the json file
    with open(json_file_path) as json_file:
        data = json.load(json_file)

        for collection_name, indexes in data.items():
            collection = database[collection_name]

            for index in indexes:
                index_fields = index["index_fields"]
                index_options = index.get("index_options", {})

                keys = [
                    (field, pymongo.TEXT) if isinstance(field, list) else (field, pymongo.ASCENDING)
                    for field in index_fields
                ]
                collection.create_index(keys, **index_options)

def main():
    client = MongoClient('mongodb://localhost:27017')
    database = create_database(client)
    folder_path = 'C:\\Users\\patel\\Desktop\\MongoDB Test\\CSV files'
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')] # condidering only the csv files

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        collection = create_collection(database, table_name)
        csv_file_path = os.path.join(folder_path, csv_file)
        insert_data(collection, csv_file_path)
        print(f"Table '{table_name}' created with data from '{csv_file}'.")

    json_file_path = 'C:\\Users\\patel\\Desktop\\MongoDB Test\\CSV files\\index.json'
    create_indexes_from_json(database, json_file_path)

if __name__ == '__main__':
    main()