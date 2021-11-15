import pandas as pd

from SmartGlovesProject_Server.Data_Prepare.spotify_utils import get_all_songs_from_df

if __name__ == '__main__':
    df_train = pd.read_csv("./resources/train.csv")
    sub_df = df_train[df_train.mood_cat == "Happy"].reset_index(drop=True)
    get_all_songs_from_df(sub_df, dest_dir="data/mp3/Happy/")

    sub_df = df_train[df_train.mood_cat == "Relaxed"].reset_index(drop=True)
    get_all_songs_from_df(sub_df, dest_dir="./resources/mp3/Relaxed")

    sub_df = df_train[df_train.mood_cat == "Angry"].reset_index(drop=True)
    get_all_songs_from_df(sub_df, dest_dir="./resources/mp3/Angry")

    sub_df = df_train[df_train.mood_cat == "Sad"].reset_index(drop=True)
    get_all_songs_from_df(sub_df, dest_dir="./resources/mp3/Sad")

