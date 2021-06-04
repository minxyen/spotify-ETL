import datetime
import requests
import pprint
import pandas as pd

from settings import USER_ID, TOKEN

USER_ID = USER_ID  # spotify username
TOKEN = TOKEN


# https://developer.spotify.com/console/get-recently-played/


def check_if_valid_data(df: pd.DataFrame):
    # Check if dataframe is empty
    if df.empty:
        print("No songs donwloaded. Finishing execution")
        return False

    # Primary Key Check -> using play at as primary key -> cuz it's unique
    if pd.Series(df['played_at']).is_unique:
        pass  # this is what we want.
    else:
        raise Exception("Primary Key Check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null valued found")

    return True



if __name__ == '__main__':

    # we need to send some information in the header with our request according to the API instruction
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)
    data = r.json()
    # pprint.pprint(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)

    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")
