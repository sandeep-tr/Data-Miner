import MySQLdb
import MySQLdb.cursors
import db_helper

#DB connection params
_RDS_HOST_ADDR = ''
_RDS_PORT = 3306
_DATABASE = 'PATIENT'

# Tables
_ADMISSION_TABLE = 'T_PATIENT_ADMISSION'


# Create a DB connection object and returns it.
def get_db():
    print 'Establishing db connection to - {}'.format(_DATABASE)
    db = MySQLdb.Connect(host=_RDS_HOST_ADDR, port=_RDS_PORT, db=_DATABASE, user='', passwd='')
    return db

def get_diagnosis_codes(age_group, sex):

    data = []
    connection = cursor = None
    query = 'SELECT ADMITTING_DIAGNOSIS_CODE FROM {}.{} \
            WHERE AGE_GROUP = %s AND SEX = %s GROUP BY ADMITTING_DIAGNOSIS_CODE'.format(_DATABASE, _ADMISSION_TABLE)
    try:
        connection = get_db()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (age_group, sex))
        
        for row in cursor.fetchall():
            data.append(dict([('diagnosis_code',row['ADMITTING_DIAGNOSIS_CODE'])]))
            
    except MySQLdb.Error, msqe:
        print msqe
        raise
    except Exception, e:
        print e
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.open:
            connection.close()
    return data

def search(age_group, sex, diagnosis):

    print 'age_group - ' + str(age_group) + ', sex - ' + str(sex) + ', diagnosis - ' + diagnosis;

    data = {}
    connection = cursor = None
    procedure = '{}.SEARCH_FACTORS'.format(_DATABASE);
    result_query = 'SELECT @_PATIENT.SEARCH_FACTORS_3, @_PATIENT.SEARCH_FACTORS_4, \
                    @_PATIENT.SEARCH_FACTORS_5, @_PATIENT.SEARCH_FACTORS_6, \
                    @_PATIENT.SEARCH_FACTORS_7, @_PATIENT.SEARCH_FACTORS_8, \
                    @_PATIENT.SEARCH_FACTORS_9'
    try:
        connection = get_db()
        cursor = connection.cursor()
        args = (age_group, sex, diagnosis, 0, 0, 0, 0, 0, 0, 0)
        cursor.callproc(procedure, args)
        cursor.execute(result_query)
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            data = {'average_stay':result[1],
                    'alive_status':result[2],
                    'average_cost':result[3],
                    'common_average_stay':result[4],
                    'common_alive_status':result[5],
                    'common_average_cost':result[6]}
        
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

def top_categories():

    data = holder = []
    connection = cursor = None
    procedure = '{}.TOP_CATEGORIES'.format(_DATABASE);
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.callproc(procedure, [])
        results = cursor.fetchall()
        
        if results:
            holder.append(db_helper.top_mortality_rate(results))
        if cursor.nextset():
            results = cursor.fetchall()
            holder.append(db_helper.top_average_charges(results))
        if cursor.nextset():
            results = cursor.fetchall()
            holder.append(db_helper.top_average_stay(results))

        data = {'top_mortality_rate': holder[0],
                'top_average_charges': holder[1],
                'top_average_stay': holder[2]}
        
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
    



    
