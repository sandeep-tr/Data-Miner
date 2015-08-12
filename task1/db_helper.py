# -*- coding: utf-8 -*-

import MySQLdb

def top_mortality_rate(results):

    data = []
    try:
        for row in results:
            data.append({'diagnosis_code' : row[0],
                         'mortality_rate' : row[1]})

            
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise

    return data     
    

def top_average_charges(results):

    data = []
    try:
        for row in results:
            data.append({'diagnosis_code' : row[0],
                         'avg_charges' : row[1]})
            
    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise

    return data 

def top_average_stay(results):

    data = []
    try:
        for row in results:
            data.append({'diagnosis_code' : row[0],
                         'avg_stay' : row[1]})

    except MySQLdb.Error, msqe:
        raise
    except Exception, e:
        raise

    return data 
    



    
