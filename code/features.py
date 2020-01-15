# shows acoustic features for tracks for the given artist

from __future__ import print_function  # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
from credentials import user_id, user_key


def create_sp():
    """
    Create
    :return:
    """
    client_credentials_manager = SpotifyClientCredentials(user_id, user_key)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    return sp


def get_song_id(sp, name_of_song, artist):
    results = sp.search(q='track:{} artist:{}'.format(name_of_song, artist), limit=2)
    return results['tracks']['items'][0]['uri']


def get_song_features(sp, song_id):
    return sp.audio_features(song_id)[0]


def get_new_features(sp):
    new_features = set()
    song_id = get_song_id(sp, 'ignorance', 'paramore')
    song_features = get_song_features(sp, song_id)
    bad_columns = ['key', 'mode', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'time_signature']
    for item in song_features:
        if item not in bad_columns:
            new_features.add(item)
    return list(new_features)


def get_song_items(sp, item):
    try:
        new_items = []
        song_id = get_song_id(sp, item['title'], item['artist_name'])
        song_features = get_song_features(sp, song_id)
        bad_columns = ['key', 'mode', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'time_signature']
        for item in song_features:
            if item not in bad_columns:
                new_items.append(song_features[item])
        return new_items
    except:
        return None


def add_features_to_dataset(dataset):
    sp = create_sp()

    new_features = get_new_features(sp)
    new_dataset = pd.DataFrame(columns=[item for item in dataset.columns] + new_features)
    i = 0
    percentage = 10
    size_of_dataset = len(dataset)
    for index in range(0, size_of_dataset):
        previous = dataset.loc[index]
        new_items = get_song_items(sp, previous)
        if (index / size_of_dataset) > percentage:
            print("Current state: " + str(percentage) + " %")
            percentage += 10
        if new_items is not None:
            new_dataset.loc[i] = [item for item in previous] + new_items
            i += 1

    return new_dataset
