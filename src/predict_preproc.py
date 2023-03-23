import pandas as pd
import numpy as np
from datetime import datetime

import elephant_conn
import course_abandon_prediction


def table_df(table: str, cur, user_id):
    cur.execute(f"SELECT * FROM {table} WHERE user_id = {user_id}")
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])




def get_data(user_id):
    # get the conection and cursor
    conn, cur = elephant_conn.elephant_conn()
    # turn tables to dfs
    consumption = table_df('consumption', cur, user_id)
    users = table_df('users', cur, user_id)
    # close connections
    cur.close()
    conn.close()
    # merge the two dfs
    return users.merge(consumption, how = 'inner', on = 'user_id')


def make_dummies(df):
    possible_identity = ['Hombre', 'Mujer', 'Otros']
    dtype = pd.CategoricalDtype(categories = possible_identity)
    identity_sr = pd.Series(df['identity'].values, dtype=dtype)
    identity_df = pd.get_dummies(identity_sr).rename(columns = {'Hombre': 'identity_Hombre', 'Mujer': 'identity_Mujer', 'Otros': 'identity_Otros'})

    possible_relationship = ['Afectado', 'Amigo', 'Familiar', 'Interesado', 'Otros', 'Profesional']
    dtype = pd.CategoricalDtype(categories = possible_relationship)
    relat_sr = pd.Series(df['hiv_relationship'].values, dtype=dtype)
    relat_df = pd.get_dummies(relat_sr).rename(columns = {'Afectado': 'hiv_relationship_Afectado',
                                                          'Amigo': 'hiv_relationship_Amigo',
                                                          'Familiar': 'hiv_relationship_Familiar',
                                                          'Interesado': 'hiv_relationship_Interesado',
                                                          'Otros': 'hiv_relationship_Otros',
                                                          'Profesional': 'hiv_relationship_Profesional'})
    
    df = pd.concat([df, identity_df, relat_df], axis = 1).drop(columns = ['identity', 'hiv_relationship'])

    return df



def return_for_predict(user_id):
    df = get_data(user_id)

    df = course_abandon_prediction.drop_columns(df)

    df = course_abandon_prediction.create_mean_time(df)

    df = course_abandon_prediction.no_courses_progress_user(df)

    df = course_abandon_prediction.no_courses_completed_user(df)

    df = course_abandon_prediction.drop_duplicates_clean(df)

    df = make_dummies(df)

    df = df.drop(columns = ['user_id', 'last_access_date'])

    return df

    

    

    