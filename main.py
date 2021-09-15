import os
import pandas as pd
import logging

from utilities.db_tools import DBMaster
from utilities.general_tools import get_dir_files_names


def create_tables_from_mappings():
    with DBMaster('cities_api_db') as db:
        mappings_path = base_path + '/db_files/mappings'
        tables_to_create = get_dir_files_names(mappings_path)
        for table_name in tables_to_create:
            db.create_table(table_name=table_name)


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    logging.info(msg="Initiated. Starting processing")

    # create necessary db tables from mappings
    create_tables_from_mappings()
    logging.info(msg="DB and tables created")

    # writing population data into db
    pop_file_path = base_path + '/populations.csv'
    population_data = pd.read_csv(pop_file_path, nrows=17059)
    with DBMaster('cities_api_db') as dbm:
        dbm.insert_df_into_table(table_name='populations', data=population_data)
