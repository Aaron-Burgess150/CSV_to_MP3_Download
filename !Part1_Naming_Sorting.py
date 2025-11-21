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


def sort_songs(filepath): #function for sorting the liked songs, both at start and after appending
    try:
        # load the dataset in
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found!")
        return None

    #sort the liked songs by Spotify ID to match the sorting method of the playlist
    sorted_liked_songs = df.sort_values(by="Spotify - id")

    return sorted_liked_songs


def find_shared_songs(liked_songs, playlist, i): #helper function to find the shared songs
    # to be ran in a for loop that calls the function and passes i as the active row in the playlist
    if playlist.iloc[i, 0] in liked_songs.iloc[:, 3].values: #if playlist song in liked songs
        return None #so the new i can be passed in
    else: #playlist song is not in liked songs, so append to liked songs
        return i


def find_in_liked_songs(liked_songs, playlist, i): #taking the song from playlist, find what row it's in in liked songs
    # NECESSARY that the song is in liked songs
    for j in range(len(liked_songs)): #go through the length of liked songs searching for the song
        if liked_songs.iloc[j, 3] == playlist.iloc[i, 0]:
            return j #returning the row the song is in in the liked songs df
        else:
            return 0 #check for a return value of 0 in the function that is calling this function
    return None


def artist_matcher(liked_songs, playlist, i, j):
    # requirement that the two songs are exactly the same, use the same i and j as last helper function to check
    if liked_songs.iloc[j, 3] == playlist.iloc[i, 0]: #if the songs share the Spotify ID
        playlist.iat[i, 2] = liked_songs.iloc[j, 1] #make the artists match, this is for searching on youtube
    else:
        print(f"Unmatched songs at row {i} in playlist, row {j} in liked songs. Please advise!")
    return


def check_sharing_and_append(liked_songs, playlist, i, j):
    # check playlist song by song and check to see if its in liked
    # if not in liked, append to the end of liked
    # check for sharing by Spotify ID
    print("hi")





if __name__ == "__main__":
    playlist = setUp_individual_playlist('Desktop\Music Project\Playlists\“make_out_chilling_tuesday_late_night”.csv')
    liked_songs = sort_songs('\Desktop\Music Project\Spotify_Liked_Songs.csv')