import pandas as pd
import numpy as np
from datetime import datetime

import elephant_conn


def table_df(table: str, cur):
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])




def get_data():
    # get the conection and cursor
    conn, cur = elephant_conn.elephant_conn()
    # turn tables to dfs
    consumption = table_df('consumption', cur)
    users = table_df('users', cur)
    # close connections
    cur.close()
    conn.close()
    # merge the two dfs
    return users.merge(consumption, how = 'inner', on = 'user_id')



def drop_columns(df):
    df = df[df['role'] == 'user']
    df = df[['user_id', 'hiv_relationship', 'age', 'identity', 'completed', 'access_date', 'last_access_date']]
    return df
    


def create_mean_time(df):
    now = datetime.now()
    
    df['time_spent_hours'] = pd.to_datetime(df['access_date']).apply(lambda x: (now - x).total_seconds() / 3600)

    mean_time_user = (df.groupby('user_id', as_index = False)['time_spent_hours']
                      .mean()
                      .rename(columns = {'time_spent_hours': 'mean_time_user_course'}))

    df = (df.merge(mean_time_user, how = 'outer', on = 'user_id')
          .drop(columns = ['time_spent_hours', 'access_date']))

    return df



def create_label(df, cutoff):
    now = datetime.now()
    
    df['time_since_login'] = pd.to_datetime(df['last_access_date']).apply(lambda x: (now - x).total_seconds() / 3600)

    df['abandoned'] = np.where(df['time_since_login'] > cutoff, 1, 0)

    abandoned = (df.groupby('user_id', as_index = False)['abandoned']
                 .max())
    
    df = df.drop(columns = ['abandoned'])

    df = (df.merge(abandoned, how = 'outer', on = 'user_id')
          .drop(columns = ['time_since_login', 'last_access_date']))

    return df


def no_courses_progress_user(df):

    no_courses_progress = (pd.DataFrame(df[df['completed'] == False]['user_id']
                                        .value_counts()).reset_index())
    
    no_courses_progress.columns = ['user_id', 'no_courses_progress']

    df = df.merge(no_courses_progress, how = 'outer', on = 'user_id').fillna(0)

    return df



def no_courses_completed_user(df):

    no_courses_completed = df.groupby('user_id', as_index = False)['completed'].sum()

    df = (df.merge(no_courses_completed, how = 'outer', on = 'user_id')
          .drop(columns = ['completed_x'])
          .rename(columns = {'completed_y': 'number_completed'}))

    return df



def drop_duplicates_clean(df):
    df = df.drop_duplicates()
    return df



def make_dummies(df):
    df = pd.get_dummies(df, columns=['identity', 'hiv_relationship'])
    return df



def create_data_aban_model():

    df = get_data()

    df = drop_columns(df)

    df = create_mean_time(df)

    df = create_label(df, 336)
        
    df = no_courses_progress_user(df)

    df = no_courses_completed_user(df)

    df = drop_duplicates_clean(df)

    df = make_dummies(df)

    user_id = df['user_id']

    y = df['abandoned']

    X = df.drop(columns = ['user_id', 'abandoned'])

    return X, y, user_id
