#!/usr/bin/env python3
import sys
import json
import logging
import os

from pathlib import Path
PARENT_DIR = Path(__file__, '../..').resolve()
sys.path.append(str(PARENT_DIR))

import hydra
import records
# This is a hidden import from records we use it to properly
# catch sql exceptions from invalid queries
import sqlalchemy
import time
from omegaconf import OmegaConf

logger = logging.getLogger("myLogger")

@hydra.main(config_path="configs", config_name="validate", version_base="1.2")
def main(cfg):
        
    for technique in ['3']:

        validation_files = os.listdir(PARENT_DIR/Path('predicted_prompt'+technique)) 
        i, vd, ivd, mtc, nmtc = 0, 0, 0, 0, 0
        valid_sql = {'match': [], 'not_matched': []}
        invalid_sql = [] 

        for file in validation_files:
            file_path = os.path.join(PARENT_DIR/Path('predicted_prompt'+technique), file)
            
            if 'example' not in file:
                continue
            
            with open(file_path) as f:
                data = json.load(f)

            db_name = data['databases']
            given_query = ' '. join(data['given_query'].split('\n'))
            predicted_query = ' '. join(data['predicted_answer'].split('\n'))

            path_to_db = 'data/database'
            db = records.Database(f'sqlite:///{path_to_db}/{db_name}/{db_name}.sqlite')
            conn = db.get_connection()

            try:
                connection = conn._conn.connect()
                given_result, predicted_result = None, None
                given_result = connection.execute(given_query).fetchall()
                time.sleep(5)
                predicted_result = connection.execute(predicted_query).fetchall()
                time.sleep(5)

                pair = {}
                pair['file'] = file
                pair['technique'] = technique
                if given_result==predicted_result:
                    valid_sql['match'].append(pair)
                    mtc+=1
                else:
                    valid_sql['not_matched'].append(pair)
                    nmtc+=1
                vd+=1

            except Exception as e:
                pair = {}
                pair['error_msg'] = str(e)
                pair['file'] = file
                pair['technique'] = technique
                invalid_sql.append(pair)
                ivd+=1
            i+=1
            print('{}/{}'.format(i, len(validation_files)), file, 'validated')

        print('\n-----------------------------------Report Technique {}--------------------------------------------'.format(technique))
        print('Number of validations done = ', len(validation_files))
        print('\n')
        print('Number of valid sql queries = ', vd)
        print('\n')
        print('Number of valid sql queries that matched = ', mtc)
        print('\n')
        print('Number of valid sql queries that did not match = ', nmtc)
        print('\n')
        print('Number of invalid sql queries = ', ivd)
        print('\n------------------------------------------------------------------------------------------------')

        with open(PARENT_DIR/Path('predicted_prompt'+technique)/Path('report_valid.json'), 'w') as f:
            json.dump(valid_sql, f, indent=4)

        with open(PARENT_DIR/Path('predicted_prompt'+technique)/Path('report_invalid.json'), 'w') as f:
            json.dump(invalid_sql, f, indent=4)


if __name__ == "__main__":
    main()