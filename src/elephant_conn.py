import configparser
import psycopg2
import os


def elephant_conn():
    '''
    Function wrapper establish the connection to the elephant SQL database
    Reads in the connection information from the config.ini file

    Returns:
    -----
        a database connection
        a cursor object to that connection
    '''
    config = configparser.ConfigParser()
    config.read('misc/config.ini')
    

    db_host = config['elesqldb']['host']
    db_port = int(config['elesqldb']['port'])
    db_username = config['elesqldb']['username']
    db_password = config['elesqldb']['password']
    db_database = config['elesqldb']['database']

    conn = psycopg2.connect(host = db_host,
                            user = db_username,
                            password = db_password,
                            port = db_port,
                            database = db_database
    )
    
    cur = conn.cursor()

    return conn, cur