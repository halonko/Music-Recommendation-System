import os
import pandas as pd


def check_if_file_exist(name_of_file):
    return os.path.isfile(name_of_file)


def check_if_directory_exist(name_of_directory):
    return os.path.exists(name_of_directory)


def create_directory(name_of_directory):
    os.mkdir(name_of_directory)


def get_dataset_from_internet(user_data_dataset_name, song_data_dataset_name):
    user_df = pd.read_table(user_data_dataset_name, header=None)
    user_df.columns = ['user_id', 'song_id', 'listen_count']
    song_df = pd.read_csv(song_data_dataset_name)
    return pd.merge(user_df, song_df.drop_duplicates(['song_id']),
                    on="song_id", how="left")


def load_dataset(dataset_directory, user_data_dataset_name,
                 song_data_dataset_name, dataset_filename):
    if not check_if_directory_exist(dataset_directory):
        create_directory(dataset_directory)

    full_filename = dataset_directory + '/' + dataset_filename
    if not check_if_file_exist(full_filename):
        dataFrame = get_dataset_from_internet(user_data_dataset_name,
                                              song_data_dataset_name)
        dataFrame.to_csv(full_filename, index=False, header=True, sep=';')
        return dataFrame
    else:
        return pd.read_csv(full_filename, sep=';')
