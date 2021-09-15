import sqlite3
import os
import pandas as pd


class DBMaster:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = self.base_path + '/../db_files/{}.db'.format(self.db_name)
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_table(self, table_name: str) -> int:
        table_mapping_path = self.base_path + '/../db_files/mappings/{}.tsv'.format(table_name)
        try:
            columns_ddl = []
            with open(table_mapping_path, 'r') as mapping_file:
                next(mapping_file)
                for line in mapping_file:
                    columns_ddl.append(line.strip().replace('\t', ' '))
        except FileNotFoundError:
            print('Mapping for table {} is not provided'.format(table_name))
            return 1
        query = 'CREATE TABLE IF NOT EXISTS {0} ({1});'.format(table_name, ', '.join(columns_ddl))
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def insert_row_into_table(self, table_name: str, columns: list, values: list, if_exists: str = 'append'):
        data = pd.DataFrame(columns=columns)
        data.loc[len(data) + 1] = values
        data.to_sql(table_name, con=self.connection, if_exists=if_exists, index=False)

    def insert_column_into_table(self, table_name: str, column: str, values: list, if_exists: str = 'append'):
        data = pd.DataFrame(values, columns=[column])
        data.to_sql(table_name, con=self.connection, if_exists=if_exists, index=False)

    def insert_df_into_table(self, table_name: str, data: pd.DataFrame, if_exists: str = 'append'):
        data.to_sql(table_name, con=self.connection, if_exists=if_exists, index=False)

    def fetch_data(self, query: str) -> list:
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def execute_dml(self, query):
        cursor = self.connection.cursor
        cursor.execute(query)
        self.connection.commit()
