"""
Gets a list of the TMDB ids for each movie using a number of different approaches.
If you save the movie id then you can more easily query the TMDB API to find movie information.
"""
import pandas as pd


def get_data_tmdbv3api(api_key, df):
    """
    Gets movie ids using the tmdbv3api library
    :param api_key: your TMDB API key
    :param df: the current dataframe
    :return: df: dataframe with values in the TMDB_id column
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
            # Takes the id from the first of the search results, if there are more than 1 film with the same title
            # this may not be the correct result!
            tmdb_id = search[0].id
            df.at[index, 'TMDB_id'] = tmdb_id
    # Convert the column to int otherwise it would be float
    df['TMDB_id'] = df['TMDB_id'].astype(int)
    return df


def get_data_requests(api_key, df):
    """
    Gets the movie ids using the requests library
    :param api_key: your TMDB API key
    :param df: the current dataframe
    :return: df: dataframe with values in the TMDB_id column
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
    # Add your TMDB V3 API key here
    api_key = ''

    # The data file as downloaded from the Moodle link only had 15 rows of data plus rows with total as well as
    # unncessary columns
    # The code below just reads in the rows and columns for that I think are needed
    cols = ['Rank', 'Film', 'Country of Origin', 'Weekend Gross', 'Distributor', '% change on last week',
            'Weeks on release', 'Number of cinemas', 'Site average', 'Total Gross to date']
    df_raw = pd.read_csv('bfi.csv', usecols=cols, skiprows=1, nrows=15)

    # Use one of the following two methods (not both!)
    df_new = get_data_tmdbv3api(api_key, df_raw)
    # df_new = get_data_requests(api_key, df_raw)

    # Remember to save the result out to a new csv file
    df_new.to_csv('bfi_with_tmdb_id.csv')
