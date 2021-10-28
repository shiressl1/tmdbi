"""
Gets a list of the TMDB ids for each movie using a number of different approaches.
If you save the movie id then you can more easily query the TMDB API to find movie information.
"""
import numpy as np
import pandas as pd


def set_pandas_display_options(df):
    """
    Set the pandas display options to the size of the dataframe
    :param df:
    :return:
    """
    pd.set_option('display.max_rows', df.shape[0] + 1)
    pd.set_option('display.max_columns', df.shape[1] + 1)


def get_data_tmdbv3api(api_key, df):
    """
    Gets movie ids using the tmdbv3api library
    :param api_key: your TMDB API key
    :param df: the current dataframe
    :return: df: dataframe with the TMDB_id column values
    """
    from tmdbv3api import TMDb, Movie
    tmdb = TMDb()
    tmdb.api_key = api_key
    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()

    for index, row in df.iterrows():
        title = row['Film']
        search = movie.search(title)
        # If there is no search result use 0 as the value
        if not search:
            df.at[index, 'TMDB_id'] = 0
        else:
            tmdb_id = search[0].id  # Crude as there may be more than 1 film with that name!
            df.at[index, 'TMDB_id'] = tmdb_id
    df['TMDB_id'] = df['TMDB_id'].astype(int)
    return df


def get_data_requests(api_key, df):
    """
    Gets the movie ids using the requests library
    :param api_key: your TMDB API key
    :param df: the current dataframe
    :return: df: dataframe with the TMDB_id column values
    """
    import requests

    url = 'https://api.themoviedb.org/3/movie/76341?api_key=' + api_key

    for index, row in df.iterrows():
        title = row['Film']
        url = 'http://api.themoviedb.org/3/search/movie?'
        params = {'api_key': api_key, 'query': title}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            json = response.json()
            if not 'results' or len(json['results']) == 0:
                df.at[index, 'TMDB_id'] = 0
            else:
                tmdb_id = json['results'][0]['id']
                df.at[index, 'TMDB_id'] = tmdb_id
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
    df['TMDB_id'] = df['TMDB_id'].astype(int)
    return df


if __name__ == '__main__':
    # Your API key here
    api_key = ''

    cols = ['Rank', 'Film', 'Country of Origin', 'Weekend Gross', 'Distributor', '% change on last week',
            'Weeks on release', 'Number of cinemas', 'Site average', 'Total Gross to date']

    df_raw = pd.read_csv('bfi.csv', usecols=cols, skiprows=1, nrows=15)

    df_new = get_data_tmdbv3api(api_key, df_raw)
    #df_new = get_data_requests(api_key, df_raw)
    df_new.to_csv('bfi_with_tmdb_id.csv')

