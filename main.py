import datetime
import requests
# import pprint
import pandas as pd

from settings import USER_ID, TOKEN


USER_ID = USER_ID  # spotify username
TOKEN = TOKEN


if __name__ == '__main__':

    # we just need to send some information in the header with our request according to the API instruction
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }


    today = datetime.datetime.now()
    # print('today:', today)
    lastyear = today - datetime.timedelta(days=365)
    # print('yesterday:', lastyear)
    lasttear_unix_timestamp = int(lastyear.timestamp()) * 1000
    # print('yesterday_unix_timestamp:', lasttear_unix_timestamp)


    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=lasttear_unix_timestamp), headers = headers)
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

