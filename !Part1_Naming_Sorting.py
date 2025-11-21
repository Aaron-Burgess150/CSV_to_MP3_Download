# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 12:48:36 2025

@author: Aaron A S Burgess
"""

import pandas as pd

# for testing and seeing the whole dataframe
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None) # Show all columns

# function to set up the individual playlist
def setUp_individual_playlist(filepath):
    try:
        # load the dataset in
        df = pd.read_csv(filepath)
    except FileNotFoundError:
       print(f"Error: File '{filepath}' not found!")
       return None
   
    
    # make the list to delete and delete those columns
    list_to_delete = ["Release Date", "Duration (ms)", "Popularity", "Explicit", "Added By", "Added At", "Genres", "Record Label", "Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Time Signature"]
    dropped_df = df.drop(list_to_delete, axis=1)


    # check for empty cells and return if there are any
    dropped_isNa_df = dropped_df.isna().any()
    if(dropped_isNa_df.sum() > 0):
        print("Missing data in important columns (Track URI, Track Name, Album Name, or Artist Name(s))")
        return None
        
    
    # rename columns in the DataFrame (not using the isna one)
    new_df = dropped_df.rename(columns={'Track URI': 'Spotify - id', 'Track Name': 'Track name', 'Album Name':'Album', 'Artist Name(s)':'Artist name'})
    
    
    # change data to drop the spotifiy:track: from the Spotify - id
    new_df["Spotify - id"] = new_df["Spotify - id"].str.replace("spotify:track:", "", regex=False)

    
    # sort the dataframe by Spotify ID
    sorted_df = new_df.sort_values(by="Spotify - id")

    # return the sorted and filtered dataframe
    return sorted_df
    
    
if __name__ == "__main__":
    playlist = setUp_individual_playlist('“make_out_chilling_tuesday_late_night”.csv')