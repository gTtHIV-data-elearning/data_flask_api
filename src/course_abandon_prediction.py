import pandas as pd
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
    df = df[['user_id', 'hiv_relationship', 'age', 'identity', 'createdat', 'completed', 'access_date']]
    return df
    

def create_mean_time(df):
    now = datetime.now()
    
    df['time_spent_hours'] = pd.to_datetime(df['access_date']).apply(lambda x: (now - x).total_seconds() / 3600)

    mean_time_user = (df.groupby('user_id', as_index = False)['time_spent_hours']
                      .mean()
                      .rename(columns = {'time_spent_hours': 'mean_time_user'}))

    df = df.merge(mean_time_user, how = 'outer', on = 'user_id').drop(columns = ['time_spent_hours'])

    return df


def no_courses_progress_user(df):
    no_courses_progress = pd.DataFrame(df[df['completed'] == False]['user_id'].value_counts()).reset_index()
    no_courses_progress.columns = ['user_id', 'no_courses_progress']

    df = df.merge(no_courses_progress, how = 'outer', on = 'user_id')

    return df



def no_courses_completed_user(df):
    no_courses_completed = pd.DataFrame(df[df['completed'] == True]['user_id'].value_counts()).reset_index()
    no_courses_completed.columns = ['user_id', 'no_courses_completed']

    df = df.merge(no_courses_completed, how = 'outer', on = 'user_id')

    return df



def drop_duplicates_clean(df):
    df = df.drop(columns = ['createdat', 'completed', 'access_date'])
    df = df.drop_duplicates()
    return df



def make_dummies(df):
    df = pd.get_dummies(df, columns=['identity', 'hiv_relationship'])
    return df









df = get_data()

df = drop_columns(df)

df = create_mean_time(df)
    
#df = no_courses_progress_user(df)

#df = no_courses_completed_user(df)

#df = drop_duplicates_clean(df)


#df = make_dummies(df)

#df.to_csv("abandono_prediccion.csv", index = False)

print(df.head())





