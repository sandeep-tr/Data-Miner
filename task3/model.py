# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors

#DB connection params
_RDS_HOST_ADDR = ''
_RDS_PORT = 3306
_DATABASE = 'PATIENT'

# Tables
_ASSOCIATION_TABLE = 'T_ASSOCIATION_TEMP'


columns = ['AGE', 'SEX', 'RACE', 'DAY_OF_ADMISSION', 'DISCHARGE_STATUS',
          'STAY_INDICATOR', 'DRG_CODE', 'LENGTH_OF_STAY', 'DRG_PRICE',
          'TOTAL_CHARGES', 'COVERED_CHARGES', 'POA_DIAGNOSIS_INDICATOR_1',
          'POA_DIAGNOSIS_INDICATOR_2', 'DIAGNOSIS_CODE_1', 'DIAGNOSIS_CODE_2',
          'PROCEDURE_CODE_1', 'PROCEDURE_CODE_2', 'DISCHARGE_DESTINATION',
          'SOURCE_OF_ADMISSION', 'TYPE_OF_ADMISSION', 'ADMITTING_DIAGNOSIS_CODE']


# Create a DB connection object and returns it.
def get_db():
    print 'Establishing db connection to - {}'.format(_DATABASE)
    db = MySQLdb.Connect(host=_RDS_HOST_ADDR, port=_RDS_PORT, db=_DATABASE, user='', passwd='')
    return db

def mine(support, confidence, csv_attributes):
    print 'support - ' + str(support) + ', confidence - ' + str(confidence) + \
          ', csv_attributes - ' + csv_attributes;

    data = []
    connection = cursor = None
    procedure = '{}.ASSOCIATION_MINING'.format(_DATABASE);

    try:
        attributes = map(int, csv_attributes.split(','))
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        for i in range(len(attributes)-1):
            for j in range(i+1, len(attributes)):
                args = (columns[attributes[i]], columns[attributes[j]])
                cursor.callproc(procedure, args)

        data = fetch_results(support, confidence, cursor)
        
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return data

def fetch_results(support, confidence, cursor):

    data = []
    query = 'SELECT ATTRIBUTE_1, ATTRIBUTE_2, VALUE_ATTRIBUTE_1, VALUE_ATTRIBUTE_2, \
            ((COUNT_COMB/TOTAL_RECORDS) * 100) AS SUPPORT, ((COUNT_COMB/COUNT_ATTRIBUTE_1) * 100) AS CONFIDENCE, \
            ((COUNT_COMB * TOTAL_RECORDS) / (COUNT_ATTRIBUTE_1 * COUNT_ATTRIBUTE_2)) AS LIFT \
            FROM {}.{} \
            WHERE ((COUNT_COMB/TOTAL_RECORDS) * 100) >= %s \
            AND ((COUNT_COMB/COUNT_ATTRIBUTE_1) * 100) >= %s \
            ORDER BY CONFIDENCE DESC'.format(_DATABASE, _ASSOCIATION_TABLE)
    try:
        cursor.execute(query, (support, confidence))
        for row in cursor.fetchall():
            data.append({'attr_1': row['ATTRIBUTE_1'],
                         'attr_2': row['ATTRIBUTE_2'],
                         'attr_1_value': row['VALUE_ATTRIBUTE_1'],
                         'attr_2_value': row['VALUE_ATTRIBUTE_2'],
                         'support': row['SUPPORT'],
                         'confidence': row['CONFIDENCE'],
                         'lift': row['LIFT']})
            

    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise

    return data
    
