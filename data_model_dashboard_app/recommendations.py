import elephant_conn
import pandas as pd
import numpy as np
from flask import jsonify


def consumption_to_df() -> pd.DataFrame:
    # establish connection and get cursor
    conn, cur = elephant_conn.elephant_conn()

    query = f'SELECT * FROM consumption'
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])


def convert_long_to_wide_df(long_df):
    # Drop the datetime column
    long_df = long_df.drop(columns = ['access_date'])
    # Now set the value to 1 for if a user has accessed certain content
    long_df['accessed'] = 1
    # now use the pivot_table to make the matrix using fill_value to put 0 when a user has not viewed content
    return long_df.pivot_table(index = 'user_id', columns = 'course_id', values = 'accessed', fill_value = 0)


def make_cosine_sim_matrix(df):
    size = len(df.columns)
    cosine_sim_matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            if i == j:
                cosine_sim_matrix[i, j] = 0.0
            else:
                dot_product = np.dot(df.values[i], df.values[j])
                norm_i = np.linalg.norm(df.values[i])
                norm_j = np.linalg.norm(df.values[j])
                if norm_i == 0 or norm_j == 0:
                    cosine_sim_matrix[i, j] = 0.0
                else:
                    cosine_sim_matrix[i, j] = dot_product / (norm_i * norm_j)

    return cosine_sim_matrix


def get_content_index(user_course_df: pd.DataFrame, content_id: str) -> int:
    '''
    This function will return the index of a given content
    '''
    return list(user_course_df.columns).index(content_id)


def check_already_seen(user_id, wide_df):
    '''
    This will simply check whether a user has already seen the potential recommendations 
    '''
    user_row = wide_df.loc[user_id]
    return [i for i, x in enumerate(user_row) if x == 1]



def find_closest_content(sim_matrix: np.ndarray, content_index: int, already_seen: list, number: int = 3) -> list:
    '''
    This will find the most similar content from the similary matrix.
    The number of results can be set and a max will be set automatically if exceeded
    Return the index of the recomendations
    '''
    if number > sim_matrix.shape[0]:
        number = sim_matrix[0]
    content_sim = sim_matrix[content_index]
    content_sim = np.delete(content_sim, already_seen)
    recom_indices = np.argsort(content_sim)[-number:][::-1].tolist()
    result = {'course_ids': recom_indices}
    return result